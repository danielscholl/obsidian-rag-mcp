"""Tests for the RAG search engine."""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from src.rag.engine import RAGEngine, SearchResult, SearchResponse


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
    
    @patch('src.rag.engine.VaultIndexer')
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
    
    @patch('src.rag.engine.VaultIndexer')
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
            'ids': [['doc1:0', 'doc2:0']],
            'documents': [['Python content', 'ML content']],
            'distances': [[0.1, 0.2]],
            'metadatas': [[
                {'source_path': 'python.md', 'title': 'Python', 'heading': '', 'tags': 'python,code', 'chunk_index': 0},
                {'source_path': 'ml.md', 'title': 'ML', 'heading': 'Intro', 'tags': 'ml,ai', 'chunk_index': 0},
            ]],
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
            assert response.results[0].source_path == 'python.md'
            assert response.results[0].score == 0.9  # 1 - 0.1
            assert response.results[1].source_path == 'ml.md'
            assert response.query == "python programming"
    
    @patch('src.rag.engine.VaultIndexer')
    def test_search_with_tag_filter(self, mock_indexer_class):
        """Test search with tag filtering."""
        mock_indexer = Mock()
        mock_indexer_class.return_value = mock_indexer
        
        mock_collection = Mock()
        mock_indexer.collection = mock_collection
        mock_collection.query.return_value = {
            'ids': [[]],
            'documents': [[]],
            'distances': [[]],
            'metadatas': [[]],
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
            assert 'where_document' in call_args.kwargs
    
    @patch('src.rag.engine.VaultIndexer')
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
            'ids': [['doc1:0', 'doc2:0', 'doc3:0']],
            'documents': [['Good match', 'OK match', 'Poor match']],
            'distances': [[0.1, 0.5, 0.9]],  # Scores: 0.9, 0.5, 0.1
            'metadatas': [[
                {'source_path': 'doc1.md', 'title': '', 'heading': '', 'tags': '', 'chunk_index': 0},
                {'source_path': 'doc2.md', 'title': '', 'heading': '', 'tags': '', 'chunk_index': 0},
                {'source_path': 'doc3.md', 'title': '', 'heading': '', 'tags': '', 'chunk_index': 0},
            ]],
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
    
    @patch('src.rag.engine.VaultIndexer')
    def test_empty_results(self, mock_indexer_class):
        """Test handling of empty results."""
        mock_indexer = Mock()
        mock_indexer_class.return_value = mock_indexer
        
        mock_collection = Mock()
        mock_indexer.collection = mock_collection
        mock_collection.query.return_value = {
            'ids': [[]],
            'documents': [[]],
            'distances': [[]],
            'metadatas': [[]],
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
    
    @patch('src.rag.engine.VaultIndexer')
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
    
    @patch('src.rag.engine.VaultIndexer')
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
    
    @patch('src.rag.engine.VaultIndexer')
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
