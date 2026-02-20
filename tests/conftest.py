"""Pytest fixtures for obsidian-rag-mcp tests."""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest


@pytest.fixture
def temp_vault():
    """Create a temporary vault directory with sample markdown files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        vault_path = Path(tmpdir)

        # Create some sample markdown files
        (vault_path / "note1.md").write_text(
            """---
title: First Note
tags: [important, test]
---

# First Note

This is the first test note. It contains important information about testing.

## Section One

Details about section one.

## Section Two

Details about section two.
"""
        )

        (vault_path / "note2.md").write_text(
            """# Second Note

This note discusses #python and #programming topics.

Some code example:

```python
def hello():
    return "world"
```
"""
        )

        # Create a subdirectory with more notes
        subdir = vault_path / "subfolder"
        subdir.mkdir()

        (subdir / "nested-note.md").write_text(
            """# Nested Note

This is a note in a subfolder. It talks about #nested #organization.
"""
        )

        # Create .obsidian directory (should be ignored)
        obsidian_dir = vault_path / ".obsidian"
        obsidian_dir.mkdir()
        (obsidian_dir / "config.json").write_text('{"theme": "dark"}')

        yield vault_path


@pytest.fixture
def temp_persist_dir():
    """Create a temporary directory for ChromaDB persistence."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_openai():
    """Mock OpenAI client for embedding tests."""
    with patch("obsidian_rag_mcp.rag.embedder.OpenAI") as mock_class:
        mock_client = Mock()
        mock_class.return_value = mock_client
        mock_client.api_key = "test-key"

        # Setup default embedding response
        def create_embeddings(**kwargs):
            texts = kwargs["input"]
            response = Mock()
            # Return deterministic embeddings based on text hash
            response.data = [
                Mock(index=i, embedding=[hash(t) % 1000 / 1000 for _ in range(1536)])
                for i, t in enumerate(texts)
            ]
            return response

        mock_client.embeddings.create.side_effect = create_embeddings

        yield mock_client


@pytest.fixture
def sample_chunks():
    """Create sample chunks for testing."""
    from obsidian_rag_mcp.rag.chunker import Chunk

    return [
        Chunk(
            content="Python is a great programming language for AI.",
            source_path="python.md",
            chunk_index=0,
            title="Python Guide",
            tags=["python", "programming"],
        ),
        Chunk(
            content="Machine learning uses data to train models.",
            source_path="ml.md",
            chunk_index=0,
            title="ML Basics",
            tags=["ml", "ai"],
        ),
        Chunk(
            content="Obsidian is a note-taking app for knowledge management.",
            source_path="tools/obsidian.md",
            chunk_index=0,
            title="Obsidian Guide",
            tags=["tools", "notes"],
        ),
    ]
