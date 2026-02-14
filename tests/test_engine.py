"""Tests for the RAG search engine."""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

from src.rag.engine import (
    ConclusionResult,
    RAGEngine,
    SearchResponse,
    SearchResult,
    SearchWithReasoningResponse,
)


class TestSearchResult:
    """Test SearchResult dataclass."""

    def test_creation(self):
        """Test creating a search result."""
        result = SearchResult(
            content="Test content",
            source_path="test.md",
            score=0.85,
            title="Test",
            heading="Section",
            tags=["tag1", "tag2"],
            chunk_index=0,
        )

        assert result.content == "Test content"
        assert result.source_path == "test.md"
        assert result.score == 0.85
        assert result.title == "Test"
        assert result.heading == "Section"
        assert result.tags == ["tag1", "tag2"]

    def test_to_dict(self):
        """Test serialization to dict."""
        result = SearchResult(
            content="Test",
            source_path="test.md",
            score=0.8567,
            title="Title",
            heading=None,
            tags=["a", "b"],
            chunk_index=1,
        )

        d = result.to_dict()
        assert d["content"] == "Test"
        assert d["score"] == 0.8567  # Rounded to 4 decimal places
        assert d["tags"] == ["a", "b"]


class TestSearchResponse:
    """Test SearchResponse dataclass."""

    def test_creation(self):
        """Test creating a search response."""
        result = SearchResult(
            content="Content",
            source_path="path.md",
            score=0.9,
            title="Title",
            heading=None,
            tags=[],
            chunk_index=0,
        )

        response = SearchResponse(
            query="test query",
            results=[result],
            total_chunks_searched=100,
        )

        assert response.query == "test query"
        assert len(response.results) == 1
        assert response.total_chunks_searched == 100

    def test_to_dict(self):
        """Test serialization to dict."""
        response = SearchResponse(
            query="query",
            results=[],
            total_chunks_searched=50,
        )

        d = response.to_dict()
        assert d["query"] == "query"
        assert d["results"] == []
        assert d["total_chunks_searched"] == 50


class TestRAGEngine:
    """Test RAGEngine with mocked dependencies."""

    @patch("src.rag.engine.VaultIndexer")
    def test_initialization(self, mock_indexer_class):
        """Test engine initialization."""
        mock_indexer = Mock()
        mock_indexer_class.return_value = mock_indexer
        mock_indexer.collection = Mock()
        mock_indexer.embedder = Mock()

        with tempfile.TemporaryDirectory() as tmpdir:
            engine = RAGEngine(
                vault_path=tmpdir,
                persist_dir=tmpdir,
                api_key="test-key",
            )

            assert engine is not None
            mock_indexer_class.assert_called_once()

    @patch("src.rag.engine.VaultIndexer")
    def test_search(self, mock_indexer_class):
        """Test search functionality."""
        # Setup mocks
        mock_indexer = Mock()
        mock_indexer_class.return_value = mock_indexer

        mock_collection = Mock()
        mock_indexer.collection = mock_collection

        mock_embedder = Mock()
        mock_indexer.embedder = mock_embedder
        mock_embedder.embed_text.return_value = [0.1] * 1536

        # Mock query results
        mock_collection.query.return_value = {
            "ids": [["doc1:0", "doc2:0"]],
            "documents": [["Python content", "ML content"]],
            "distances": [[0.1, 0.2]],
            "metadatas": [
                [
                    {
                        "source_path": "python.md",
                        "title": "Python",
                        "heading": "",
                        "tags": "python,code",
                        "chunk_index": 0,
                    },
                    {
                        "source_path": "ml.md",
                        "title": "ML",
                        "heading": "Intro",
                        "tags": "ml,ai",
                        "chunk_index": 0,
                    },
                ]
            ],
        }
        mock_collection.count.return_value = 10

        with tempfile.TemporaryDirectory() as tmpdir:
            engine = RAGEngine(
                vault_path=tmpdir,
                persist_dir=tmpdir,
                api_key="test-key",
            )

            response = engine.search("python programming")

            assert len(response.results) == 2
            assert response.results[0].source_path == "python.md"
            assert response.results[0].score == 0.9  # 1 - 0.1
            assert response.results[1].source_path == "ml.md"
            assert response.query == "python programming"

    @patch("src.rag.engine.VaultIndexer")
    def test_search_with_tag_filter(self, mock_indexer_class):
        """Test search with tag filtering."""
        mock_indexer = Mock()
        mock_indexer_class.return_value = mock_indexer

        mock_collection = Mock()
        mock_indexer.collection = mock_collection
        mock_collection.query.return_value = {
            "ids": [[]],
            "documents": [[]],
            "distances": [[]],
            "metadatas": [[]],
        }
        mock_collection.count.return_value = 0

        mock_embedder = Mock()
        mock_indexer.embedder = mock_embedder
        mock_embedder.embed_text.return_value = [0.1] * 1536

        with tempfile.TemporaryDirectory() as tmpdir:
            engine = RAGEngine(
                vault_path=tmpdir,
                persist_dir=tmpdir,
                api_key="test-key",
            )

            engine.search("query", tags=["python"])

            # Check that where_document filter was passed
            call_args = mock_collection.query.call_args
            assert "where_document" in call_args.kwargs

    @patch("src.rag.engine.VaultIndexer")
    def test_min_score_filtering(self, mock_indexer_class):
        """Test that results below min_score are filtered."""
        mock_indexer = Mock()
        mock_indexer_class.return_value = mock_indexer

        mock_collection = Mock()
        mock_indexer.collection = mock_collection

        mock_embedder = Mock()
        mock_indexer.embedder = mock_embedder
        mock_embedder.embed_text.return_value = [0.1] * 1536

        # Return results with varying distances
        mock_collection.query.return_value = {
            "ids": [["doc1:0", "doc2:0", "doc3:0"]],
            "documents": [["Good match", "OK match", "Poor match"]],
            "distances": [[0.1, 0.5, 0.9]],  # Scores: 0.9, 0.5, 0.1
            "metadatas": [
                [
                    {
                        "source_path": "doc1.md",
                        "title": "",
                        "heading": "",
                        "tags": "",
                        "chunk_index": 0,
                    },
                    {
                        "source_path": "doc2.md",
                        "title": "",
                        "heading": "",
                        "tags": "",
                        "chunk_index": 0,
                    },
                    {
                        "source_path": "doc3.md",
                        "title": "",
                        "heading": "",
                        "tags": "",
                        "chunk_index": 0,
                    },
                ]
            ],
        }
        mock_collection.count.return_value = 3

        with tempfile.TemporaryDirectory() as tmpdir:
            engine = RAGEngine(
                vault_path=tmpdir,
                persist_dir=tmpdir,
                api_key="test-key",
            )

            response = engine.search("query", min_score=0.4)

            # Only results with score >= 0.4 should be returned
            assert len(response.results) == 2
            assert all(r.score >= 0.4 for r in response.results)

    @patch("src.rag.engine.VaultIndexer")
    def test_empty_results(self, mock_indexer_class):
        """Test handling of empty results."""
        mock_indexer = Mock()
        mock_indexer_class.return_value = mock_indexer

        mock_collection = Mock()
        mock_indexer.collection = mock_collection
        mock_collection.query.return_value = {
            "ids": [[]],
            "documents": [[]],
            "distances": [[]],
            "metadatas": [[]],
        }
        mock_collection.count.return_value = 0

        mock_embedder = Mock()
        mock_indexer.embedder = mock_embedder
        mock_embedder.embed_text.return_value = [0.1] * 1536

        with tempfile.TemporaryDirectory() as tmpdir:
            engine = RAGEngine(
                vault_path=tmpdir,
                persist_dir=tmpdir,
                api_key="test-key",
            )

            response = engine.search("nonexistent topic")

            assert response.results == []
            assert response.query == "nonexistent topic"

    @patch("src.rag.engine.VaultIndexer")
    def test_get_note(self, mock_indexer_class):
        """Test getting a note by path."""
        mock_indexer = Mock()
        mock_indexer_class.return_value = mock_indexer
        mock_indexer.collection = Mock()
        mock_indexer.embedder = Mock()

        with tempfile.TemporaryDirectory() as tmpdir:
            vault = Path(tmpdir)

            # Create a test note
            test_note = vault / "test-note.md"
            test_note.write_text("# Test\n\nContent here.")

            engine = RAGEngine(
                vault_path=tmpdir,
                persist_dir=tmpdir,
                api_key="test-key",
            )

            content = engine.get_note("test-note.md")

            assert content == "# Test\n\nContent here."

    @patch("src.rag.engine.VaultIndexer")
    def test_get_note_nonexistent(self, mock_indexer_class):
        """Test getting a nonexistent note."""
        mock_indexer = Mock()
        mock_indexer_class.return_value = mock_indexer
        mock_indexer.collection = Mock()
        mock_indexer.embedder = Mock()

        with tempfile.TemporaryDirectory() as tmpdir:
            engine = RAGEngine(
                vault_path=tmpdir,
                persist_dir=tmpdir,
                api_key="test-key",
            )

            content = engine.get_note("nonexistent.md")

            assert content is None

    @patch("src.rag.engine.VaultIndexer")
    def test_get_note_path_traversal_blocked(self, mock_indexer_class):
        """Test that path traversal attempts are blocked."""
        mock_indexer = Mock()
        mock_indexer_class.return_value = mock_indexer
        mock_indexer.collection = Mock()
        mock_indexer.embedder = Mock()

        with tempfile.TemporaryDirectory() as tmpdir:
            engine = RAGEngine(
                vault_path=tmpdir,
                persist_dir=tmpdir,
                api_key="test-key",
            )

            # Try to access file outside vault
            content = engine.get_note("../../../etc/passwd")

            assert content is None

    @patch("src.rag.engine.VaultIndexer")
    def test_search_empty_query_raises_error(self, mock_indexer_class):
        """Test that empty query raises ValueError."""
        mock_indexer = Mock()
        mock_indexer_class.return_value = mock_indexer
        mock_indexer.collection = Mock()
        mock_indexer.embedder = Mock()

        with tempfile.TemporaryDirectory() as tmpdir:
            engine = RAGEngine(
                vault_path=tmpdir,
                persist_dir=tmpdir,
                api_key="test-key",
            )

            import pytest

            with pytest.raises(ValueError, match="Query cannot be empty"):
                engine.search("")

            with pytest.raises(ValueError, match="Query cannot be empty"):
                engine.search("   ")

    @patch("src.rag.engine.VaultIndexer")
    def test_search_invalid_top_k_raises_error(self, mock_indexer_class):
        """Test that invalid top_k values raise ValueError."""
        mock_indexer = Mock()
        mock_indexer_class.return_value = mock_indexer
        mock_indexer.collection = Mock()
        mock_indexer.embedder = Mock()

        with tempfile.TemporaryDirectory() as tmpdir:
            engine = RAGEngine(
                vault_path=tmpdir,
                persist_dir=tmpdir,
                api_key="test-key",
            )

            import pytest

            with pytest.raises(ValueError, match="top_k must be at least 1"):
                engine.search("valid query", top_k=0)

            with pytest.raises(ValueError, match="top_k must be at least 1"):
                engine.search("valid query", top_k=-1)

            with pytest.raises(ValueError, match="top_k cannot exceed 50"):
                engine.search("valid query", top_k=51)


class TestConclusionResult:
    """Test ConclusionResult dataclass."""

    def test_creation(self):
        """Test creating a conclusion result."""
        result = ConclusionResult(
            id="abc123",
            type="deductive",
            statement="Python uses indentation",
            confidence=0.95,
            evidence=["whitespace matters"],
            source_path="python.md",
            heading="Syntax",
        )

        assert result.id == "abc123"
        assert result.type == "deductive"
        assert result.confidence == 0.95

    def test_to_dict(self):
        """Test serialization to dict."""
        result = ConclusionResult(
            id="xyz",
            type="inductive",
            statement="Pattern observed",
            confidence=0.7567,
            evidence=["evidence1", "evidence2"],
            source_path="notes.md",
            heading=None,
        )

        d = result.to_dict()
        assert d["id"] == "xyz"
        assert d["type"] == "inductive"
        assert d["confidence"] == 0.7567
        assert d["evidence"] == ["evidence1", "evidence2"]


class TestSearchWithReasoningResponse:
    """Test SearchWithReasoningResponse dataclass."""

    def test_creation(self):
        """Test creating a response."""
        search_result = SearchResult(
            content="Content",
            source_path="test.md",
            score=0.9,
            title="Title",
            heading=None,
            tags=[],
            chunk_index=0,
        )
        conclusion = ConclusionResult(
            id="c1",
            type="deductive",
            statement="Statement",
            confidence=0.9,
            evidence=[],
            source_path="test.md",
            heading=None,
        )

        response = SearchWithReasoningResponse(
            query="test",
            results=[search_result],
            conclusions=[conclusion],
            total_chunks_searched=100,
            total_conclusions_searched=50,
        )

        assert response.query == "test"
        assert len(response.results) == 1
        assert len(response.conclusions) == 1
        assert response.total_conclusions_searched == 50

    def test_to_dict(self):
        """Test serialization to dict."""
        response = SearchWithReasoningResponse(
            query="query",
            results=[],
            conclusions=[],
            total_chunks_searched=10,
            total_conclusions_searched=5,
        )

        d = response.to_dict()
        assert d["query"] == "query"
        assert d["results"] == []
        assert d["conclusions"] == []
        assert d["total_conclusions_searched"] == 5


class TestSearchWithReasoning:
    """Test search_with_reasoning functionality."""

    @patch("src.rag.engine.VaultIndexer")
    def test_returns_empty_conclusions_when_reasoning_disabled(
        self, mock_indexer_class
    ):
        """Test search_with_reasoning returns empty conclusions when disabled."""
        mock_indexer = Mock()
        mock_indexer_class.return_value = mock_indexer
        mock_indexer.conclusion_store = None

        mock_collection = Mock()
        mock_indexer.collection = mock_collection
        mock_collection.query.return_value = {
            "ids": [["doc1:0"]],
            "documents": [["Content"]],
            "distances": [[0.1]],
            "metadatas": [
                [
                    {
                        "source_path": "doc.md",
                        "title": "",
                        "heading": "",
                        "tags": "",
                        "chunk_index": 0,
                    }
                ]
            ],
        }
        mock_collection.count.return_value = 1

        mock_embedder = Mock()
        mock_indexer.embedder = mock_embedder
        mock_embedder.embed_text.return_value = [0.1] * 1536

        with tempfile.TemporaryDirectory() as tmpdir:
            engine = RAGEngine(
                vault_path=tmpdir,
                persist_dir=tmpdir,
                api_key="test-key",
                reasoning_enabled=False,
            )

            response = engine.search_with_reasoning("test query")

            assert len(response.results) == 1
            assert response.conclusions == []
            assert response.total_conclusions_searched == 0

    @patch("src.rag.engine.VaultIndexer")
    def test_returns_conclusions_when_reasoning_enabled(self, mock_indexer_class):
        """Test search_with_reasoning returns conclusions when enabled."""
        mock_indexer = Mock()
        mock_indexer_class.return_value = mock_indexer

        # Mock conclusion store
        mock_conclusion_store = Mock()
        mock_indexer.conclusion_store = mock_conclusion_store
        mock_conclusion_store.count.return_value = 10

        # Create mock conclusion
        mock_conclusion = Mock()
        mock_conclusion.id = "c1"
        mock_conclusion.type = Mock()
        mock_conclusion.type.value = "deductive"
        mock_conclusion.statement = "Test conclusion"
        mock_conclusion.confidence = 0.9
        mock_conclusion.evidence = ["evidence"]
        mock_conclusion.context = Mock()
        mock_conclusion.context.source_path = "doc.md"
        mock_conclusion.context.heading = "Section"

        mock_conclusion_store.search.return_value = [mock_conclusion]

        mock_collection = Mock()
        mock_indexer.collection = mock_collection
        mock_collection.query.return_value = {
            "ids": [["doc1:0"]],
            "documents": [["Content"]],
            "distances": [[0.1]],
            "metadatas": [
                [
                    {
                        "source_path": "doc.md",
                        "title": "",
                        "heading": "",
                        "tags": "",
                        "chunk_index": 0,
                    }
                ]
            ],
        }
        mock_collection.count.return_value = 1

        mock_embedder = Mock()
        mock_indexer.embedder = mock_embedder
        mock_embedder.embed_text.return_value = [0.1] * 1536

        with tempfile.TemporaryDirectory() as tmpdir:
            engine = RAGEngine(
                vault_path=tmpdir,
                persist_dir=tmpdir,
                api_key="test-key",
                reasoning_enabled=True,
            )
            # Manually set conclusion_store since we're mocking
            engine.conclusion_store = mock_conclusion_store

            response = engine.search_with_reasoning("test query")

            assert len(response.results) == 1
            assert len(response.conclusions) == 1
            assert response.conclusions[0].statement == "Test conclusion"
            assert response.conclusions[0].type == "deductive"
            assert response.total_conclusions_searched == 10


class TestGetConclusionTrace:
    """Test get_conclusion_trace functionality."""

    @patch("src.rag.engine.VaultIndexer")
    def test_returns_none_when_reasoning_disabled(self, mock_indexer_class):
        """Test returns None when reasoning is disabled."""
        mock_indexer = Mock()
        mock_indexer_class.return_value = mock_indexer
        mock_indexer.conclusion_store = None
        mock_indexer.collection = Mock()
        mock_indexer.embedder = Mock()

        with tempfile.TemporaryDirectory() as tmpdir:
            engine = RAGEngine(
                vault_path=tmpdir,
                persist_dir=tmpdir,
                api_key="test-key",
                reasoning_enabled=False,
            )

            result = engine.get_conclusion_trace("nonexistent")
            assert result is None

    @patch("src.rag.engine.VaultIndexer")
    def test_returns_none_for_nonexistent_conclusion(self, mock_indexer_class):
        """Test returns None when conclusion not found."""
        mock_indexer = Mock()
        mock_indexer_class.return_value = mock_indexer

        mock_conclusion_store = Mock()
        mock_conclusion_store.get.return_value = None
        mock_indexer.conclusion_store = mock_conclusion_store
        mock_indexer.collection = Mock()
        mock_indexer.embedder = Mock()

        with tempfile.TemporaryDirectory() as tmpdir:
            engine = RAGEngine(
                vault_path=tmpdir,
                persist_dir=tmpdir,
                api_key="test-key",
                reasoning_enabled=True,
            )
            engine.conclusion_store = mock_conclusion_store

            result = engine.get_conclusion_trace("nonexistent")
            assert result is None

    @patch("src.rag.engine.VaultIndexer")
    def test_returns_trace_for_valid_conclusion(self, mock_indexer_class):
        """Test returns trace for valid conclusion."""
        mock_indexer = Mock()
        mock_indexer_class.return_value = mock_indexer

        # Create mock conclusion
        mock_conclusion = Mock()
        mock_conclusion.id = "c1"
        mock_conclusion.source_chunk_id = "chunk1"
        mock_conclusion.confidence = 0.9
        mock_conclusion.context = Mock()
        mock_conclusion.context.source_path = "test.md"
        mock_conclusion.to_dict.return_value = {
            "id": "c1",
            "statement": "Test conclusion",
            "confidence": 0.9,
        }

        mock_conclusion_store = Mock()
        mock_conclusion_store.get.return_value = mock_conclusion
        mock_conclusion_store.find_similar.return_value = []
        mock_indexer.conclusion_store = mock_conclusion_store

        # Mock collection for source chunk lookup
        mock_collection = Mock()
        mock_collection.get.return_value = {
            "ids": ["chunk1"],
            "documents": ["Source content"],
            "metadatas": [
                {
                    "source_path": "test.md",
                    "title": "Test",
                    "heading": "",
                    "tags": "",
                    "chunk_index": 0,
                }
            ],
        }
        mock_indexer.collection = mock_collection
        mock_indexer.embedder = Mock()

        with tempfile.TemporaryDirectory() as tmpdir:
            engine = RAGEngine(
                vault_path=tmpdir,
                persist_dir=tmpdir,
                api_key="test-key",
                reasoning_enabled=True,
            )
            engine.conclusion_store = mock_conclusion_store
            engine.collection = mock_collection

            result = engine.get_conclusion_trace("c1")

            assert result is not None
            assert "conclusion" in result
            assert "supporting_evidence" in result
            assert "parent_conclusions" in result
            assert "child_conclusions" in result
            assert "confidence_path" in result


class TestExploreConnectedConclusions:
    """Test explore_connected_conclusions functionality."""

    @patch("src.rag.engine.VaultIndexer")
    def test_returns_empty_when_reasoning_disabled(self, mock_indexer_class):
        """Test returns empty list when reasoning disabled."""
        mock_indexer = Mock()
        mock_indexer_class.return_value = mock_indexer
        mock_indexer.conclusion_store = None
        mock_indexer.collection = Mock()
        mock_indexer.embedder = Mock()

        with tempfile.TemporaryDirectory() as tmpdir:
            engine = RAGEngine(
                vault_path=tmpdir,
                persist_dir=tmpdir,
                api_key="test-key",
                reasoning_enabled=False,
            )

            result = engine.explore_connected_conclusions(query="test")
            assert result == []

    @patch("src.rag.engine.VaultIndexer")
    def test_search_by_query(self, mock_indexer_class):
        """Test searching by query text."""
        mock_indexer = Mock()
        mock_indexer_class.return_value = mock_indexer

        mock_conclusion = Mock()
        mock_conclusion.confidence = 0.9
        mock_conclusion.to_dict.return_value = {"id": "c1", "statement": "Found"}

        mock_conclusion_store = Mock()
        mock_conclusion_store.search.return_value = [mock_conclusion]
        mock_indexer.conclusion_store = mock_conclusion_store
        mock_indexer.collection = Mock()
        mock_indexer.embedder = Mock()

        with tempfile.TemporaryDirectory() as tmpdir:
            engine = RAGEngine(
                vault_path=tmpdir,
                persist_dir=tmpdir,
                api_key="test-key",
                reasoning_enabled=True,
            )
            engine.conclusion_store = mock_conclusion_store

            result = engine.explore_connected_conclusions(query="test query")

            assert len(result) == 1
            assert result[0]["relationship"] == "matches_query"
            mock_conclusion_store.search.assert_called_once()
