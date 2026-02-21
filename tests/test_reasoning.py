"""Tests for the reasoning layer."""

import json
import tempfile
from unittest.mock import Mock, patch

from obsidian_rag_mcp.reasoning.conclusion_store import ConclusionStore
from obsidian_rag_mcp.reasoning.extractor import ConclusionExtractor, ExtractorConfig
from obsidian_rag_mcp.reasoning.models import (
    ChunkContext,
    Conclusion,
    ConclusionType,
)


class TestConclusionType:
    """Test ConclusionType enum."""

    def test_values(self):
        """Test enum values."""
        assert ConclusionType.DEDUCTIVE.value == "deductive"
        assert ConclusionType.INDUCTIVE.value == "inductive"
        assert ConclusionType.ABDUCTIVE.value == "abductive"

    def test_from_string(self):
        """Test creating from string."""
        assert ConclusionType("deductive") == ConclusionType.DEDUCTIVE
        assert ConclusionType("inductive") == ConclusionType.INDUCTIVE


class TestChunkContext:
    """Test ChunkContext dataclass."""

    def test_creation(self):
        """Test creating a context."""
        ctx = ChunkContext(
            source_path="notes/python.md",
            title="Python Basics",
            heading="Variables",
            tags=["python", "tutorial"],
            chunk_index=0,
        )
        assert ctx.source_path == "notes/python.md"
        assert ctx.tags == ["python", "tutorial"]

    def test_to_dict(self):
        """Test serialization."""
        ctx = ChunkContext(
            source_path="test.md",
            title="Test",
            heading=None,
            tags=[],
            chunk_index=1,
        )
        d = ctx.to_dict()
        assert d["source_path"] == "test.md"
        assert d["heading"] is None


class TestConclusion:
    """Test Conclusion dataclass."""

    def test_creation(self):
        """Test creating a conclusion."""
        ctx = ChunkContext(
            source_path="test.md",
            title="Test",
            heading="Section",
            tags=["tag1"],
            chunk_index=0,
        )
        conclusion = Conclusion(
            id="abc123",
            type=ConclusionType.DEDUCTIVE,
            statement="Python uses indentation for blocks",
            confidence=0.95,
            evidence=["indentation for blocks", "whitespace matters"],
            source_chunk_id="chunk1",
            context=ctx,
        )
        assert conclusion.type == ConclusionType.DEDUCTIVE
        assert conclusion.confidence == 0.95
        assert len(conclusion.evidence) == 2

    def test_to_dict(self):
        """Test serialization."""
        ctx = ChunkContext(
            source_path="test.md",
            title="Test",
            heading=None,
            tags=[],
            chunk_index=0,
        )
        conclusion = Conclusion(
            id="xyz789",
            type=ConclusionType.INDUCTIVE,
            statement="Most Python files use .py extension",
            confidence=0.8,
            evidence=["observed pattern"],
            source_chunk_id="chunk2",
            context=ctx,
        )
        d = conclusion.to_dict()
        assert d["type"] == "inductive"
        assert d["confidence"] == 0.8

    def test_from_dict(self):
        """Test deserialization."""
        data = {
            "id": "test123",
            "type": "deductive",
            "statement": "Test statement",
            "confidence": 0.9,
            "evidence": ["evidence1"],
            "source_chunk_id": "chunk1",
            "context": {
                "source_path": "test.md",
                "title": "Test",
                "heading": "H1",
                "tags": ["a", "b"],
                "chunk_index": 0,
            },
        }
        conclusion = Conclusion.from_dict(data)
        assert conclusion.id == "test123"
        assert conclusion.type == ConclusionType.DEDUCTIVE
        assert conclusion.context.heading == "H1"


class TestExtractorConfig:
    """Test ExtractorConfig."""

    def test_defaults(self):
        """Test default configuration."""
        config = ExtractorConfig()
        assert config.model == "gpt-4.1-mini"
        assert config.extract_deductive is True
        assert config.extract_abductive is False

    def test_custom(self):
        """Test custom configuration."""
        config = ExtractorConfig(
            model="gpt-4o",
            min_confidence=0.7,
            extract_abductive=True,
        )
        assert config.model == "gpt-4o"
        assert config.min_confidence == 0.7


class TestConclusionExtractor:
    """Test ConclusionExtractor with mocked OpenAI."""

    @patch("obsidian_rag_mcp.reasoning.extractor._create_openai_client")
    def test_extract_conclusions(self, mock_openai_class):
        """Test extracting conclusions from a chunk."""
        # Setup mock
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        mock_client.api_key = "test-key"

        mock_response = Mock()
        mock_response.choices = [
            Mock(
                message=Mock(
                    content=json.dumps(
                        {
                            "conclusions": [
                                {
                                    "type": "deductive",
                                    "statement": "Python requires indentation",
                                    "confidence": 0.95,
                                    "evidence": ["uses indentation"],
                                }
                            ]
                        }
                    )
                )
            )
        ]
        mock_client.chat.completions.create.return_value = mock_response

        # Test
        extractor = ConclusionExtractor(api_key="test-key")
        ctx = ChunkContext(
            source_path="python.md",
            title="Python",
            heading="Syntax",
            tags=["python"],
            chunk_index=0,
        )

        conclusions = extractor.extract_conclusions(
            chunk="Python uses indentation for code blocks.",
            chunk_id="chunk1",
            context=ctx,
        )

        assert len(conclusions) == 1
        assert conclusions[0].type == ConclusionType.DEDUCTIVE
        assert conclusions[0].confidence == 0.95

    @patch("obsidian_rag_mcp.reasoning.extractor._create_openai_client")
    def test_empty_chunk_returns_empty(self, mock_openai_class):
        """Test that empty chunks return no conclusions."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        mock_client.api_key = "test-key"

        extractor = ConclusionExtractor(api_key="test-key")
        ctx = ChunkContext(
            source_path="test.md",
            title="Test",
            heading=None,
            tags=[],
            chunk_index=0,
        )

        conclusions = extractor.extract_conclusions(
            chunk="",
            chunk_id="chunk1",
            context=ctx,
        )

        assert conclusions == []
        mock_client.chat.completions.create.assert_not_called()

    @patch("obsidian_rag_mcp.reasoning.extractor._create_openai_client")
    def test_filters_low_confidence(self, mock_openai_class):
        """Test that low confidence conclusions are filtered."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        mock_client.api_key = "test-key"

        mock_response = Mock()
        mock_response.choices = [
            Mock(
                message=Mock(
                    content=json.dumps(
                        {
                            "conclusions": [
                                {
                                    "type": "deductive",
                                    "statement": "High conf",
                                    "confidence": 0.9,
                                    "evidence": [],
                                },
                                {
                                    "type": "deductive",
                                    "statement": "Low conf",
                                    "confidence": 0.3,
                                    "evidence": [],
                                },
                            ]
                        }
                    )
                )
            )
        ]
        mock_client.chat.completions.create.return_value = mock_response

        config = ExtractorConfig(min_confidence=0.5)
        extractor = ConclusionExtractor(api_key="test-key", config=config)
        ctx = ChunkContext(
            source_path="test.md",
            title="Test",
            heading=None,
            tags=[],
            chunk_index=0,
        )

        conclusions = extractor.extract_conclusions(
            chunk="Some content",
            chunk_id="chunk1",
            context=ctx,
        )

        assert len(conclusions) == 1
        assert conclusions[0].statement == "High conf"

    @patch("obsidian_rag_mcp.reasoning.extractor._create_openai_client")
    def test_batch_extraction(self, mock_openai_class):
        """Test batch extraction of multiple chunks."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        mock_client.api_key = "test-key"

        mock_response = Mock()
        mock_response.choices = [
            Mock(
                message=Mock(
                    content=json.dumps(
                        {
                            "results": {
                                "chunk1": {
                                    "conclusions": [
                                        {
                                            "type": "deductive",
                                            "statement": "Conclusion from chunk 1",
                                            "confidence": 0.9,
                                            "evidence": ["evidence1"],
                                        }
                                    ]
                                },
                                "chunk2": {
                                    "conclusions": [
                                        {
                                            "type": "inductive",
                                            "statement": "Conclusion from chunk 2",
                                            "confidence": 0.8,
                                            "evidence": ["evidence2"],
                                        }
                                    ]
                                },
                            }
                        }
                    )
                )
            )
        ]
        mock_client.chat.completions.create.return_value = mock_response

        extractor = ConclusionExtractor(api_key="test-key")

        ctx1 = ChunkContext(
            source_path="doc1.md",
            title="Doc 1",
            heading="Section",
            tags=["tag1"],
            chunk_index=0,
        )
        ctx2 = ChunkContext(
            source_path="doc2.md",
            title="Doc 2",
            heading="Section",
            tags=["tag2"],
            chunk_index=0,
        )

        chunks = [
            ("Content of chunk 1", "chunk1", ctx1),
            ("Content of chunk 2", "chunk2", ctx2),
        ]

        results = extractor.extract_conclusions_batch(chunks)

        assert len(results) == 2
        assert "chunk1" in results
        assert "chunk2" in results
        assert len(results["chunk1"]) == 1
        assert len(results["chunk2"]) == 1
        assert results["chunk1"][0].statement == "Conclusion from chunk 1"
        assert results["chunk2"][0].statement == "Conclusion from chunk 2"
        # Only one API call for both chunks
        assert mock_client.chat.completions.create.call_count == 1

    @patch("obsidian_rag_mcp.reasoning.extractor._create_openai_client")
    def test_deterministic_ids_same_statement_same_source(self, mock_openai_class):
        """Same statement + same source always produces same ID."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        mock_client.api_key = "test-key"

        extractor = ConclusionExtractor(api_key="test-key")

        id1 = extractor._generate_id("Database error occurred", "chunk1")
        id2 = extractor._generate_id("Database error occurred", "chunk1")

        assert id1 == id2

    @patch("obsidian_rag_mcp.reasoning.extractor._create_openai_client")
    def test_deterministic_ids_different_statements(self, mock_openai_class):
        """Different statements produce different IDs."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        mock_client.api_key = "test-key"

        extractor = ConclusionExtractor(api_key="test-key")

        id1 = extractor._generate_id("Database error occurred", "chunk1")
        id2 = extractor._generate_id("Network connection failed", "chunk1")

        assert id1 != id2

    @patch("obsidian_rag_mcp.reasoning.extractor._create_openai_client")
    def test_deterministic_ids_same_statement_different_source(self, mock_openai_class):
        """Same statement from different sources produces different IDs (provenance)."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        mock_client.api_key = "test-key"

        extractor = ConclusionExtractor(api_key="test-key")

        id1 = extractor._generate_id("Database error occurred", "chunk_from_note_a")
        id2 = extractor._generate_id("Database error occurred", "chunk_from_note_b")

        assert id1 != id2

    @patch("obsidian_rag_mcp.reasoning.extractor._create_openai_client")
    def test_deterministic_ids_case_insensitive(self, mock_openai_class):
        """IDs are case-insensitive for deduplication."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        mock_client.api_key = "test-key"

        extractor = ConclusionExtractor(api_key="test-key")

        id1 = extractor._generate_id("Database error", "chunk1")
        id2 = extractor._generate_id("database error", "chunk1")
        id3 = extractor._generate_id("DATABASE ERROR", "chunk1")

        assert id1 == id2
        assert id2 == id3

    @patch("obsidian_rag_mcp.reasoning.extractor._create_openai_client")
    def test_deterministic_ids_whitespace_normalized(self, mock_openai_class):
        """IDs are whitespace-normalized for deduplication."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        mock_client.api_key = "test-key"

        extractor = ConclusionExtractor(api_key="test-key")

        id1 = extractor._generate_id("Database error", "chunk1")
        id2 = extractor._generate_id("  Database error  ", "chunk1")

        assert id1 == id2


class TestConclusionStore:
    """Test ConclusionStore with real ChromaDB (temp dir)."""

    def test_add_and_get(self):
        """Test adding and retrieving conclusions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ConclusionStore(persist_dir=tmpdir)

            ctx = ChunkContext(
                source_path="test.md",
                title="Test",
                heading="Section",
                tags=["tag1"],
                chunk_index=0,
            )
            conclusion = Conclusion(
                id="test123",
                type=ConclusionType.DEDUCTIVE,
                statement="Test conclusion",
                confidence=0.9,
                evidence=["evidence"],
                source_chunk_id="chunk1",
                context=ctx,
            )

            store.add([conclusion])

            retrieved = store.get("test123")
            assert retrieved is not None
            assert retrieved.statement == "Test conclusion"
            assert retrieved.type == ConclusionType.DEDUCTIVE

    def test_count(self):
        """Test counting conclusions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ConclusionStore(persist_dir=tmpdir)
            assert store.count() == 0

            ctx = ChunkContext(
                source_path="test.md",
                title="Test",
                heading=None,
                tags=[],
                chunk_index=0,
            )
            conclusions = [
                Conclusion(
                    id=f"id{i}",
                    type=ConclusionType.DEDUCTIVE,
                    statement=f"Conclusion {i}",
                    confidence=0.9,
                    evidence=[],
                    source_chunk_id="chunk1",
                    context=ctx,
                )
                for i in range(3)
            ]
            store.add(conclusions)

            assert store.count() == 3

    def test_get_by_source(self):
        """Test filtering by source file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ConclusionStore(persist_dir=tmpdir)

            conclusions = []
            for i, path in enumerate(["a.md", "a.md", "b.md"]):
                ctx = ChunkContext(
                    source_path=path,
                    title="Test",
                    heading=None,
                    tags=[],
                    chunk_index=0,
                )
                conclusions.append(
                    Conclusion(
                        id=f"id{i}",
                        type=ConclusionType.DEDUCTIVE,
                        statement=f"From {path}",
                        confidence=0.9,
                        evidence=[],
                        source_chunk_id=f"chunk{i}",
                        context=ctx,
                    )
                )
            store.add(conclusions)

            a_conclusions = store.get_by_source("a.md")
            assert len(a_conclusions) == 2

            b_conclusions = store.get_by_source("b.md")
            assert len(b_conclusions) == 1

    def test_delete_by_source(self):
        """Test deleting by source file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ConclusionStore(persist_dir=tmpdir)

            conclusions = []
            for i, path in enumerate(["a.md", "a.md", "b.md"]):
                ctx = ChunkContext(
                    source_path=path,
                    title="Test",
                    heading=None,
                    tags=[],
                    chunk_index=0,
                )
                conclusions.append(
                    Conclusion(
                        id=f"id{i}",
                        type=ConclusionType.DEDUCTIVE,
                        statement=f"From {path}",
                        confidence=0.9,
                        evidence=[],
                        source_chunk_id=f"chunk{i}",
                        context=ctx,
                    )
                )
            store.add(conclusions)

            deleted = store.delete_by_source("a.md")
            assert deleted == 2
            assert store.count() == 1

    def test_clear(self):
        """Test clearing all conclusions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ConclusionStore(persist_dir=tmpdir)

            ctx = ChunkContext(
                source_path="test.md",
                title="Test",
                heading=None,
                tags=[],
                chunk_index=0,
            )
            store.add(
                [
                    Conclusion(
                        id="id1",
                        type=ConclusionType.DEDUCTIVE,
                        statement="Test",
                        confidence=0.9,
                        evidence=[],
                        source_chunk_id="chunk1",
                        context=ctx,
                    )
                ]
            )

            assert store.count() == 1
            store.clear()
            assert store.count() == 0

    def test_search_without_embedder(self):
        """Test text-based search without embedder."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ConclusionStore(persist_dir=tmpdir)

            ctx = ChunkContext(
                source_path="python.md",
                title="Python",
                heading="Basics",
                tags=["python"],
                chunk_index=0,
            )
            conclusions = [
                Conclusion(
                    id="id1",
                    type=ConclusionType.DEDUCTIVE,
                    statement="Python uses indentation for code blocks",
                    confidence=0.95,
                    evidence=["whitespace matters"],
                    source_chunk_id="chunk1",
                    context=ctx,
                ),
                Conclusion(
                    id="id2",
                    type=ConclusionType.INDUCTIVE,
                    statement="Most Python files use .py extension",
                    confidence=0.8,
                    evidence=["observed pattern"],
                    source_chunk_id="chunk2",
                    context=ctx,
                ),
            ]
            store.add(conclusions)

            # Search should find relevant conclusions
            results = store.search("indentation", top_k=5)
            assert len(results) >= 1

    def test_search_with_filters(self):
        """Test search with type and confidence filters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ConclusionStore(persist_dir=tmpdir)

            conclusions = []
            for i, (ctype, conf) in enumerate(
                [
                    (ConclusionType.DEDUCTIVE, 0.9),
                    (ConclusionType.INDUCTIVE, 0.7),
                    (ConclusionType.DEDUCTIVE, 0.5),
                ]
            ):
                ctx = ChunkContext(
                    source_path="test.md",
                    title="Test",
                    heading=None,
                    tags=[],
                    chunk_index=i,
                )
                conclusions.append(
                    Conclusion(
                        id=f"id{i}",
                        type=ctype,
                        statement=f"Conclusion {i} about testing",
                        confidence=conf,
                        evidence=[],
                        source_chunk_id=f"chunk{i}",
                        context=ctx,
                    )
                )
            store.add(conclusions)

            # Filter by type
            deductive = store.search(
                "testing",
                conclusion_type=ConclusionType.DEDUCTIVE,
            )
            assert all(c.type == ConclusionType.DEDUCTIVE for c in deductive)

            # Filter by min confidence
            high_conf = store.search("testing", min_confidence=0.8)
            assert all(c.confidence >= 0.8 for c in high_conf)

    def test_roundtrip_preserves_context(self):
        """Test that title and chunk_index survive storage round-trip."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ConclusionStore(persist_dir=tmpdir)

            ctx = ChunkContext(
                source_path="guide.md",
                title="Python Guide",
                heading="Chapter 1",
                tags=["python", "tutorial"],
                chunk_index=5,
            )
            original = Conclusion(
                id="roundtrip1",
                type=ConclusionType.DEDUCTIVE,
                statement="Test roundtrip",
                confidence=0.9,
                evidence=["evidence"],
                source_chunk_id="chunk5",
                context=ctx,
            )
            store.add([original])

            retrieved = store.get("roundtrip1")
            assert retrieved is not None
            assert retrieved.context.title == "Python Guide"
            assert retrieved.context.chunk_index == 5
            assert retrieved.context.heading == "Chapter 1"
            assert retrieved.context.tags == ["python", "tutorial"]

    @patch("obsidian_rag_mcp.reasoning.conclusion_store.chromadb.PersistentClient")
    def test_search_confidence_filter_in_query(self, mock_client_class):
        """Test that confidence filter is included in ChromaDB where clause."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        mock_collection = Mock()
        mock_client.get_or_create_collection.return_value = mock_collection

        # Setup mock response
        mock_collection.query.return_value = {
            "ids": [["id1"]],
            "documents": [["Test conclusion"]],
            "metadatas": [
                [
                    {
                        "type": "deductive",
                        "confidence": 0.9,
                        "source_chunk_id": "chunk1",
                        "source_path": "test.md",
                        "title": "Test",
                        "heading": "",
                        "tags": "",
                        "chunk_index": 0,
                        "evidence": "[]",
                        "related_conclusions": "",
                        "created_at": "",
                    }
                ]
            ],
            "distances": [[0.1]],
        }

        store = ConclusionStore(persist_dir="/tmp/test")

        # Search with min_confidence
        store.search("test query", min_confidence=0.8)

        # Verify the where clause includes confidence filter
        call_args = mock_collection.query.call_args
        where_clause = call_args.kwargs.get("where")
        assert where_clause is not None
        assert where_clause == {"confidence": {"$gte": 0.8}}

        # Verify n_results is exactly top_k (not top_k * 2)
        n_results = call_args.kwargs.get("n_results")
        assert n_results == 10  # default top_k

    @patch("obsidian_rag_mcp.reasoning.conclusion_store.chromadb.PersistentClient")
    def test_search_fetches_exact_top_k(self, mock_client_class):
        """Test that search fetches exactly top_k results, not more."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        mock_collection = Mock()
        mock_client.get_or_create_collection.return_value = mock_collection

        mock_collection.query.return_value = {
            "ids": [[]],
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]],
        }

        store = ConclusionStore(persist_dir="/tmp/test")

        # Search with specific top_k
        store.search("test query", top_k=5)

        # Verify n_results matches top_k exactly
        call_args = mock_collection.query.call_args
        n_results = call_args.kwargs.get("n_results")
        assert n_results == 5

    @patch("obsidian_rag_mcp.reasoning.conclusion_store.chromadb.PersistentClient")
    def test_search_multi_type_uses_in_operator(self, mock_client_class):
        """Test that multiple conclusion types use $in operator in ChromaDB."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        mock_collection = Mock()
        mock_client.get_or_create_collection.return_value = mock_collection

        mock_collection.query.return_value = {
            "ids": [[]],
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]],
        }

        store = ConclusionStore(persist_dir="/tmp/test")

        # Search with multiple types
        store.search(
            "test query",
            conclusion_types=[ConclusionType.DEDUCTIVE, ConclusionType.INDUCTIVE],
        )

        # Verify the where clause uses $in operator
        call_args = mock_collection.query.call_args
        where_clause = call_args.kwargs.get("where")
        assert where_clause is not None
        assert where_clause == {"type": {"$in": ["deductive", "inductive"]}}

    @patch("obsidian_rag_mcp.reasoning.conclusion_store.chromadb.PersistentClient")
    def test_search_single_type_from_list(self, mock_client_class):
        """Test that single type in list doesn't use $in operator."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        mock_collection = Mock()
        mock_client.get_or_create_collection.return_value = mock_collection

        mock_collection.query.return_value = {
            "ids": [[]],
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]],
        }

        store = ConclusionStore(persist_dir="/tmp/test")

        # Search with single type in list
        store.search(
            "test query",
            conclusion_types=[ConclusionType.DEDUCTIVE],
        )

        # Verify the where clause is simple equality, not $in
        call_args = mock_collection.query.call_args
        where_clause = call_args.kwargs.get("where")
        assert where_clause is not None
        assert where_clause == {"type": "deductive"}

    @patch("obsidian_rag_mcp.reasoning.conclusion_store.chromadb.PersistentClient")
    def test_search_multiple_filters_uses_and_operator(self, mock_client_class):
        """Test that multiple filters are combined with $and operator."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        mock_collection = Mock()
        mock_client.get_or_create_collection.return_value = mock_collection

        mock_collection.query.return_value = {
            "ids": [[]],
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]],
        }

        store = ConclusionStore(persist_dir="/tmp/test")

        # Search with both conclusion_types and min_confidence
        store.search(
            "test query",
            conclusion_types=[ConclusionType.DEDUCTIVE, ConclusionType.INDUCTIVE],
            min_confidence=0.8,
        )

        # Verify the where clause uses $and operator with both filters
        call_args = mock_collection.query.call_args
        where_clause = call_args.kwargs.get("where")
        assert where_clause is not None
        assert "$and" in where_clause
        assert len(where_clause["$and"]) == 2
        assert {"type": {"$in": ["deductive", "inductive"]}} in where_clause["$and"]
        assert {"confidence": {"$gte": 0.8}} in where_clause["$and"]
