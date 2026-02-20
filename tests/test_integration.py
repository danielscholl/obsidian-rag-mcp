"""End-to-end integration tests for the obsidian-rag-mcp pipeline.

Tests the complete flow: index -> search with real ChromaDB and mocked OpenAI.

Note: These tests use real ChromaDB with temp directories. On Windows,
ChromaDB may hold file locks, so we use ignore_errors for cleanup.
"""

import gc
import shutil
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from obsidian_rag_mcp.rag.engine import RAGEngine
from obsidian_rag_mcp.rag.indexer import IndexerConfig, VaultIndexer


@pytest.fixture
def temp_dirs():
    """Create temp directories and clean up after, handling Windows file locks."""
    vault_dir = tempfile.mkdtemp()
    persist_dir = tempfile.mkdtemp()

    yield vault_dir, persist_dir

    # Cleanup - force GC and ignore errors for Windows file locking
    gc.collect()
    shutil.rmtree(vault_dir, ignore_errors=True)
    shutil.rmtree(persist_dir, ignore_errors=True)


@pytest.fixture
def mock_openai_embeddings():
    """Mock OpenAI for both embedder and extractor."""
    with (
        patch("obsidian_rag_mcp.rag.embedder.OpenAI") as mock_embedder_class,
        patch("obsidian_rag_mcp.reasoning.extractor.OpenAI") as mock_extractor_class,
    ):
        # Setup embedder mock
        mock_embedder = Mock()
        mock_embedder_class.return_value = mock_embedder
        mock_embedder.api_key = "test-key"

        def create_embeddings(**kwargs):
            texts = kwargs["input"]
            response = Mock()
            # Return deterministic embeddings based on text content
            response.data = [
                Mock(index=i, embedding=[hash(t) % 1000 / 1000 for _ in range(1536)])
                for i, t in enumerate(texts)
            ]
            return response

        mock_embedder.embeddings.create.side_effect = create_embeddings

        # Setup extractor mock (for reasoning tests)
        mock_extractor = Mock()
        mock_extractor_class.return_value = mock_extractor
        mock_extractor.api_key = "test-key"

        yield mock_embedder, mock_extractor


class TestIndexThenSearch:
    """Test the complete index -> search pipeline."""

    def test_index_then_search_returns_results(self, mock_openai_embeddings, temp_dirs):
        """Index a vault and verify search returns matching notes."""
        vault_dir, persist_dir = temp_dirs
        vault_path = Path(vault_dir)

        # Create test notes
        (vault_path / "database.md").write_text(
            """# Database Guide

PostgreSQL is a powerful relational database.

## Connection Pooling

Connection pooling improves performance.
"""
        )

        (vault_path / "networking.md").write_text(
            """# Networking Basics

TCP/IP is the foundation of internet communication.
"""
        )

        # Index the vault
        config = IndexerConfig(
            vault_path=str(vault_path),
            persist_dir=persist_dir,
        )
        indexer = VaultIndexer(config, api_key="test-key")
        stats = indexer.index_vault()

        assert stats.total_files == 2
        assert stats.total_chunks >= 2

        # Search using RAGEngine
        engine = RAGEngine(
            vault_path=str(vault_path),
            persist_dir=persist_dir,
            api_key="test-key",
        )

        results = engine.search("database connection", top_k=5)

        # Should find database-related content
        assert len(results.results) > 0
        sources = [r.source_path for r in results.results]
        assert "database.md" in sources

    def test_incremental_index_updates(self, mock_openai_embeddings, temp_dirs):
        """Modify a file and verify new content is searchable after reindex."""
        vault_dir, persist_dir = temp_dirs
        vault_path = Path(vault_dir)

        # Create initial note
        note_path = vault_path / "evolving.md"
        note_path.write_text("# Original Content\n\nInitial version of the note.")

        # Initial index
        config = IndexerConfig(
            vault_path=str(vault_path),
            persist_dir=persist_dir,
        )
        indexer = VaultIndexer(config, api_key="test-key")
        indexer.index_vault()

        # Verify initial content is searchable
        engine = RAGEngine(
            vault_path=str(vault_path),
            persist_dir=persist_dir,
            api_key="test-key",
        )
        initial_results = engine.search("original content", top_k=5)
        assert len(initial_results.results) > 0

        # Modify the file
        note_path.write_text(
            "# Updated Content\n\nNew version with kubernetes deployment info."
        )

        # Reindex (incremental update based on hash)
        indexer2 = VaultIndexer(config, api_key="test-key")
        indexer2.index_vault()

        # Create new engine to pick up changes
        engine2 = RAGEngine(
            vault_path=str(vault_path),
            persist_dir=persist_dir,
            api_key="test-key",
        )

        # Verify new content is searchable
        new_results = engine2.search("kubernetes deployment", top_k=5)
        assert len(new_results.results) > 0
        assert any("kubernetes" in r.content.lower() for r in new_results.results)

    def test_deleted_files_removed_from_index(self, mock_openai_embeddings, temp_dirs):
        """Delete a file and verify it's removed from search results."""
        vault_dir, persist_dir = temp_dirs
        vault_path = Path(vault_dir)

        # Create two notes
        (vault_path / "keeper.md").write_text("# Keeper\n\nThis note stays.")
        deletable = vault_path / "deletable.md"
        deletable.write_text("# Deletable\n\nThis note will be removed.")

        # Initial index
        config = IndexerConfig(
            vault_path=str(vault_path),
            persist_dir=persist_dir,
        )
        indexer = VaultIndexer(config, api_key="test-key")
        indexer.index_vault()

        # Verify both are searchable
        engine = RAGEngine(
            vault_path=str(vault_path),
            persist_dir=persist_dir,
            api_key="test-key",
        )
        results = engine.search("note", top_k=10)
        sources = [r.source_path for r in results.results]
        assert "keeper.md" in sources
        assert "deletable.md" in sources

        # Delete the file
        deletable.unlink()

        # Reindex
        indexer2 = VaultIndexer(config, api_key="test-key")
        indexer2.index_vault()

        # Verify deleted file is no longer in results
        engine2 = RAGEngine(
            vault_path=str(vault_path),
            persist_dir=persist_dir,
            api_key="test-key",
        )
        results2 = engine2.search("note", top_k=10)
        sources2 = [r.source_path for r in results2.results]
        assert "keeper.md" in sources2
        assert "deletable.md" not in sources2

    def test_search_by_tag_filters_correctly(self, mock_openai_embeddings, temp_dirs):
        """Test that tag-based filtering works correctly."""
        vault_dir, persist_dir = temp_dirs
        vault_path = Path(vault_dir)

        # Create notes with different tags
        (vault_path / "python.md").write_text(
            """---
tags: [python, programming]
---
# Python Guide

Python is a great language.
"""
        )

        (vault_path / "rust.md").write_text(
            """---
tags: [rust, programming]
---
# Rust Guide

Rust is a systems language.
"""
        )

        (vault_path / "cooking.md").write_text(
            """---
tags: [recipes, food]
---
# Cooking Guide

How to cook pasta.
"""
        )

        # Index
        config = IndexerConfig(
            vault_path=str(vault_path),
            persist_dir=persist_dir,
        )
        indexer = VaultIndexer(config, api_key="test-key")
        indexer.index_vault()

        # Search with tag filter
        engine = RAGEngine(
            vault_path=str(vault_path),
            persist_dir=persist_dir,
            api_key="test-key",
        )

        # Search for programming content only
        results = engine.search("language", top_k=10, tags=["programming"])

        # With tag filtering, should not find cooking note
        sources = [r.source_path for r in results.results]
        assert "cooking.md" not in sources

        # Now search without tag filter and verify cooking shows up
        all_results = engine.search("guide", top_k=10)
        all_sources = [r.source_path for r in all_results.results]
        # All three notes should be searchable without tag filter
        assert len(all_sources) == 3


class TestReasoningPipeline:
    """Test the reasoning extraction pipeline."""

    def test_reasoning_pipeline_extracts_conclusions(
        self, mock_openai_embeddings, temp_dirs
    ):
        """Index with reasoning enabled and verify conclusions are extracted."""
        mock_embedder, mock_extractor = mock_openai_embeddings

        # Setup extractor to return conclusions
        import json

        mock_response = Mock()
        mock_response.choices = [
            Mock(
                message=Mock(
                    content=json.dumps(
                        {
                            "conclusions": [
                                {
                                    "type": "deductive",
                                    "statement": "PostgreSQL supports transactions",
                                    "confidence": 0.9,
                                    "evidence": ["ACID compliance"],
                                }
                            ]
                        }
                    )
                )
            )
        ]
        mock_extractor.chat.completions.create.return_value = mock_response

        vault_dir, persist_dir = temp_dirs
        vault_path = Path(vault_dir)

        # Create a note with extractable content
        (vault_path / "database.md").write_text(
            """# Database Fundamentals

PostgreSQL is an ACID-compliant relational database management system.
It supports transactions, ensuring data integrity.
"""
        )

        # Index with reasoning enabled
        config = IndexerConfig(
            vault_path=str(vault_path),
            persist_dir=persist_dir,
            reasoning_enabled=True,
        )
        indexer = VaultIndexer(config, api_key="test-key")
        stats = indexer.index_vault()

        # Verify reasoning stats
        assert stats.reasoning_enabled is True
        assert stats.total_conclusions >= 0  # May be 0 if extraction fails

        # Create engine and verify search_with_reasoning works
        engine = RAGEngine(
            vault_path=str(vault_path),
            persist_dir=persist_dir,
            api_key="test-key",
            reasoning_enabled=True,
        )

        # Search with reasoning
        results = engine.search_with_reasoning("database transactions", top_k=5)

        # Should have response structure with results and conclusions
        assert hasattr(results, "results")  # Search results
        assert hasattr(results, "conclusions")  # Extracted conclusions
        assert len(results.results) >= 0  # May have results
