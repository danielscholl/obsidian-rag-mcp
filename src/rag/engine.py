"""
RAG Engine - Query and retrieval for semantic search.

Supports optional reasoning layer for enriched search with logical conclusions.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from .indexer import IndexerConfig, VaultIndexer

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from src.reasoning import ConclusionStore
    from src.reasoning.extractor import ExtractorConfig
    from src.reasoning.models import ConclusionType


@dataclass
class SearchResult:
    """A single search result."""

    content: str
    source_path: str
    title: str
    heading: str | None
    tags: list[str]
    score: float  # Similarity score (0-1, higher is better)
    chunk_index: int

    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "source_path": self.source_path,
            "title": self.title,
            "heading": self.heading,
            "tags": self.tags,
            "score": round(self.score, 4),
            "chunk_index": self.chunk_index,
        }


@dataclass
class SearchResponse:
    """Response from a search query."""

    query: str
    results: list[SearchResult]
    total_chunks_searched: int

    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "results": [r.to_dict() for r in self.results],
            "total_chunks_searched": self.total_chunks_searched,
        }


@dataclass
class SourceEvidence:
    """Source chunk that supports a conclusion."""

    chunk_id: str
    content: str
    source_path: str
    title: str
    heading: str | None

    def to_dict(self) -> dict:
        return {
            "chunk_id": self.chunk_id,
            "content": self.content,
            "source_path": self.source_path,
            "title": self.title,
            "heading": self.heading,
        }


@dataclass
class ConclusionResult:
    """A conclusion result for search_with_reasoning."""

    id: str
    type: str
    statement: str
    confidence: float
    evidence: list[str]
    source_path: str
    heading: str | None
    source_chunk: SourceEvidence | None = None  # The chunk this conclusion came from
    related_conclusions: list[str] | None = None  # IDs of related conclusions

    def to_dict(self) -> dict:
        result = {
            "id": self.id,
            "type": self.type,
            "statement": self.statement,
            "confidence": round(self.confidence, 4),
            "evidence": self.evidence,
            "source_path": self.source_path,
            "heading": self.heading,
        }
        if self.source_chunk:
            result["source_chunk"] = self.source_chunk.to_dict()
        if self.related_conclusions:
            result["related_conclusions"] = self.related_conclusions
        return result


@dataclass
class SearchWithReasoningResponse:
    """Response from search_with_reasoning."""

    query: str
    results: list[SearchResult]
    conclusions: list[ConclusionResult]
    total_chunks_searched: int
    total_conclusions_searched: int

    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "results": [r.to_dict() for r in self.results],
            "conclusions": [c.to_dict() for c in self.conclusions],
            "total_chunks_searched": self.total_chunks_searched,
            "total_conclusions_searched": self.total_conclusions_searched,
        }


class RAGEngine:
    """
    Query engine for semantic search over indexed vault.

    Features:
    - Semantic similarity search
    - Tag-based filtering
    - Result ranking and formatting
    - Optional reasoning layer with conclusion search
    """

    def __init__(
        self,
        vault_path: str,
        persist_dir: str = ".chroma",
        api_key: str | None = None,
        reasoning_enabled: bool = False,
        extractor_config: ExtractorConfig | None = None,
    ):
        self.vault_path = Path(vault_path).resolve()
        self.reasoning_enabled = reasoning_enabled

        # Initialize indexer (which gives us access to ChromaDB)
        self.indexer = VaultIndexer(
            config=IndexerConfig(
                vault_path=vault_path,
                persist_dir=persist_dir,
                reasoning_enabled=reasoning_enabled,
                extractor_config=extractor_config,
            ),
            api_key=api_key,
        )

        # Use the same embedder for queries
        self.embedder = self.indexer.embedder
        self.collection = self.indexer.collection

        # Access reasoning components from indexer
        self.conclusion_store: ConclusionStore | None = self.indexer.conclusion_store

    def _get_source_chunk(self, chunk_id: str) -> SourceEvidence | None:
        """Fetch source chunk content for a conclusion."""
        try:
            result = self.collection.get(
                ids=[chunk_id],
                include=["documents", "metadatas"],
            )
            if result["ids"]:
                metadata = result["metadatas"][0]
                return SourceEvidence(
                    chunk_id=chunk_id,
                    content=result["documents"][0],
                    source_path=metadata["source_path"],
                    title=metadata.get("title", ""),
                    heading=metadata.get("heading"),
                )
        except Exception as e:
            logger.debug(f"Could not fetch source chunk {chunk_id}: {e}")
        return None

    def search(
        self,
        query: str,
        top_k: int = 5,
        tags: list[str] | None = None,
        min_score: float = 0.0,
    ) -> SearchResponse:
        """
        Semantic search across the vault.

        Args:
            query: Natural language search query
            top_k: Maximum number of results to return (1-50)
            tags: Optional list of tags to filter by (OR logic)
            min_score: Minimum similarity score (0-1)

        Returns:
            SearchResponse with ranked results

        Raises:
            ValueError: If query is empty or top_k is out of bounds
        """
        # Validate inputs
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")
        if top_k < 1:
            raise ValueError("top_k must be at least 1")
        if top_k > 50:
            raise ValueError("top_k cannot exceed 50")

        # Embed the query
        query_embedding = self.embedder.embed_text(query)

        # Build where clause for filtering
        where_document = None
        if tags:
            # Filter by tags using where_document (searches in document text)
            # This is a workaround since ChromaDB doesn't have $contains for metadata
            # We'll search for tags in the content instead
            tag_patterns = [f"#{tag}" for tag in tags]
            # Use $or with $contains on where_document
            if len(tag_patterns) == 1:
                where_document = {"$contains": tag_patterns[0]}
            else:
                where_document = {"$or": [{"$contains": t} for t in tag_patterns]}

        # Query ChromaDB
        try:
            query_kwargs = {
                "query_embeddings": [query_embedding],
                "n_results": top_k * 2,  # Get extra for score filtering
                "include": ["documents", "metadatas", "distances"],
            }
            if where_document:
                query_kwargs["where_document"] = where_document

            results = self.collection.query(**query_kwargs)
        except Exception as e:
            # Handle empty collection
            if "empty" in str(e).lower():
                return SearchResponse(
                    query=query,
                    results=[],
                    total_chunks_searched=0,
                )
            raise

        # Process results
        search_results = []

        if results["ids"] and results["ids"][0]:
            for i, doc_id in enumerate(results["ids"][0]):
                # Convert distance to similarity score (cosine distance to similarity)
                distance = results["distances"][0][i]
                score = 1 - distance  # Cosine distance to similarity

                if score < min_score:
                    continue

                metadata = results["metadatas"][0][i]
                content = results["documents"][0][i]

                # Parse tags back from comma-separated string
                tags_str = metadata.get("tags", "")
                tags_list = [t.strip() for t in tags_str.split(",") if t.strip()]

                search_results.append(
                    SearchResult(
                        content=content,
                        source_path=metadata["source_path"],
                        title=metadata.get("title", ""),
                        heading=metadata.get("heading") or None,
                        tags=tags_list,
                        score=score,
                        chunk_index=metadata.get("chunk_index", 0),
                    )
                )

        # Sort by score and limit
        search_results.sort(key=lambda r: r.score, reverse=True)
        search_results = search_results[:top_k]

        return SearchResponse(
            query=query,
            results=search_results,
            total_chunks_searched=self.collection.count(),
        )

    def search_with_reasoning(
        self,
        query: str,
        top_k: int = 5,
        conclusion_types: list[str] | None = None,
        min_confidence: float = 0.0,
        tags: list[str] | None = None,
    ) -> SearchWithReasoningResponse:
        """
        Search with reasoning layer - returns chunks AND relevant conclusions.

        Args:
            query: Natural language search query
            top_k: Maximum number of chunk results to return
            conclusion_types: Filter conclusions by type ('deductive', 'inductive', 'abductive')
            min_confidence: Minimum confidence for conclusions (0-1)
            tags: Optional list of tags to filter by

        Returns:
            SearchWithReasoningResponse with chunks and conclusions
        """
        # First do regular search
        search_response = self.search(query=query, top_k=top_k, tags=tags)

        # If reasoning not enabled or no store, return without conclusions
        if not self.conclusion_store:
            return SearchWithReasoningResponse(
                query=query,
                results=search_response.results,
                conclusions=[],
                total_chunks_searched=search_response.total_chunks_searched,
                total_conclusions_searched=0,
            )

        # Import ConclusionType for filtering
        from src.reasoning.models import ConclusionType

        # Parse conclusion type filter
        type_filter_list: list[ConclusionType] | None = None
        if conclusion_types:
            valid_types = []
            for type_str in conclusion_types:
                try:
                    valid_types.append(ConclusionType(type_str))
                except ValueError:
                    pass  # Invalid type, skip
            if valid_types:
                type_filter_list = valid_types

        # Search conclusions with type filter pushed to ChromaDB
        raw_conclusions = self.conclusion_store.search(
            query=query,
            top_k=top_k,
            conclusion_types=type_filter_list,
            min_confidence=min_confidence,
        )

        # Convert to ConclusionResult with source chunks and related conclusions
        conclusion_results = []
        for c in raw_conclusions:
            # Get source chunk content
            source_chunk = self._get_source_chunk(c.source_chunk_id)

            # Find related conclusions (semantically similar)
            related_ids = []
            try:
                related = self.conclusion_store.search(
                    query=c.statement,
                    top_k=3,
                    min_confidence=min_confidence,
                )
                related_ids = [r.id for r in related if r.id != c.id][:2]
            except Exception as e:
                logger.debug(f"Could not find related conclusions: {e}")

            conclusion_results.append(
                ConclusionResult(
                    id=c.id,
                    type=c.type.value,
                    statement=c.statement,
                    confidence=c.confidence,
                    evidence=c.evidence,
                    source_path=c.context.source_path,
                    heading=c.context.heading,
                    source_chunk=source_chunk,
                    related_conclusions=related_ids if related_ids else None,
                )
            )

        return SearchWithReasoningResponse(
            query=query,
            results=search_response.results,
            conclusions=conclusion_results,
            total_chunks_searched=search_response.total_chunks_searched,
            total_conclusions_searched=self.conclusion_store.count(),
        )

    def get_conclusion_trace(
        self,
        conclusion_id: str,
        max_depth: int = 3,
    ) -> dict | None:
        """
        Get the reasoning trace for a specific conclusion.

        Shows the evidence chain: source chunk -> conclusion -> related conclusions.

        Args:
            conclusion_id: ID of the conclusion to trace
            max_depth: Maximum depth for finding related conclusions

        Returns:
            ReasoningTrace as dict, or None if conclusion not found
        """
        if not self.conclusion_store:
            return None

        # Get the target conclusion
        conclusion = self.conclusion_store.get(conclusion_id)
        if not conclusion:
            return None

        # Get the source chunk as supporting evidence
        supporting_evidence = []
        try:
            chunk_result = self.collection.get(
                ids=[conclusion.source_chunk_id],
                include=["documents", "metadatas"],
            )
            if chunk_result["ids"]:
                metadata = chunk_result["metadatas"][0]
                tags_str = metadata.get("tags", "")
                tags = [t.strip() for t in tags_str.split(",") if t.strip()]

                supporting_evidence.append(
                    {
                        "chunk_id": conclusion.source_chunk_id,
                        "content": chunk_result["documents"][0],
                        "relevance_score": 1.0,
                        "context": {
                            "source_path": metadata["source_path"],
                            "title": metadata.get("title", ""),
                            "heading": metadata.get("heading") or None,
                            "tags": tags,
                            "chunk_index": metadata.get("chunk_index", 0),
                        },
                    }
                )
        except Exception as e:
            logger.debug(
                f"Could not retrieve source chunk {conclusion.source_chunk_id}: {e}"
            )

        # Find related conclusions (semantically similar)
        similar = self.conclusion_store.find_similar(
            conclusion_id, top_k=max_depth * 2, exclude_same_source=False
        )

        # Separate into "parent" (from same source, likely supporting)
        # and "child" (from different sources, likely derived/extended)
        parent_conclusions = []
        child_conclusions = []

        for related, similarity in similar:
            conclusion_dict = related.to_dict()
            conclusion_dict["similarity"] = round(similarity, 4)

            if related.context.source_path == conclusion.context.source_path:
                parent_conclusions.append(conclusion_dict)
            else:
                child_conclusions.append(conclusion_dict)

            if (
                len(parent_conclusions) >= max_depth
                and len(child_conclusions) >= max_depth
            ):
                break

        # Calculate confidence path (product of confidences)
        confidence_path = conclusion.confidence
        for parent in parent_conclusions[:max_depth]:
            confidence_path *= parent.get("confidence", 1.0)

        return {
            "conclusion": conclusion.to_dict(),
            "supporting_evidence": supporting_evidence,
            "parent_conclusions": parent_conclusions[:max_depth],
            "child_conclusions": child_conclusions[:max_depth],
            "confidence_path": round(confidence_path, 4),
        }

    def explore_connected_conclusions(
        self,
        query: str | None = None,
        conclusion_id: str | None = None,
        top_k: int = 10,
        min_confidence: float = 0.0,
    ) -> list[dict]:
        """
        Explore conclusions related to a query or another conclusion.

        Args:
            query: Text query to find related conclusions
            conclusion_id: ID of conclusion to find related ones
            top_k: Maximum number of conclusions to return
            min_confidence: Minimum confidence threshold

        Returns:
            List of ConnectedConclusion dicts
        """
        if not self.conclusion_store:
            return []

        connected = []

        if conclusion_id:
            # Find similar to a specific conclusion
            similar = self.conclusion_store.find_similar(
                conclusion_id, top_k=top_k, exclude_same_source=False
            )

            target = self.conclusion_store.get(conclusion_id)
            target_source = target.context.source_path if target else None

            for conclusion, similarity in similar:
                if conclusion.confidence < min_confidence:
                    continue

                # Determine relationship based on source
                if conclusion.context.source_path == target_source:
                    relationship = "same_source"
                else:
                    relationship = "similar"

                # Find shared evidence (source chunks)
                shared = []
                if target and target.source_chunk_id == conclusion.source_chunk_id:
                    shared.append(conclusion.source_chunk_id)

                connected.append(
                    {
                        "conclusion": conclusion.to_dict(),
                        "relationship": relationship,
                        "strength": round(similarity, 4),
                        "shared_evidence": shared,
                    }
                )

        elif query:
            # Search by query text
            conclusions = self.conclusion_store.search(
                query=query, top_k=top_k, min_confidence=min_confidence
            )

            for conclusion in conclusions:
                connected.append(
                    {
                        "conclusion": conclusion.to_dict(),
                        "relationship": "matches_query",
                        "strength": conclusion.confidence,
                        "shared_evidence": [],
                    }
                )

        return connected

    def get_note(self, path: str) -> str | None:
        """
        Get the full content of a note by path.

        Args:
            path: Relative path within the vault

        Returns:
            Note content or None if not found
        """
        full_path = (self.vault_path / path).resolve()

        # Security: check path containment FIRST (before revealing existence)
        if not full_path.is_relative_to(self.vault_path):
            return None  # Path traversal attempt

        if not full_path.exists():
            return None

        return full_path.read_text(encoding="utf-8")

    def get_related(
        self,
        path: str,
        top_k: int = 5,
    ) -> SearchResponse:
        """
        Find notes related to a given note.

        Args:
            path: Path to the source note
            top_k: Number of related notes to return

        Returns:
            SearchResponse with related notes
        """
        content = self.get_note(path)
        if not content:
            return SearchResponse(
                query=f"related to: {path}",
                results=[],
                total_chunks_searched=0,
            )

        # Use the note content as the query
        # Truncate if too long
        query_text = content[:8000]

        # Search and exclude the source note
        response = self.search(query_text, top_k=top_k + 5)

        # Filter out chunks from the same file
        filtered_results = [r for r in response.results if r.source_path != path][
            :top_k
        ]

        return SearchResponse(
            query=f"related to: {path}",
            results=filtered_results,
            total_chunks_searched=response.total_chunks_searched,
        )

    def list_recent(self, limit: int = 10) -> list[dict]:
        """
        List recently modified notes.

        Returns list of dicts with path and mtime.
        """
        files = self.indexer.scan_vault()

        # Get modification times
        file_info = []
        for path in files:
            stat = path.stat()
            rel_path = str(path.relative_to(self.vault_path))
            file_info.append(
                {
                    "path": rel_path,
                    "modified": stat.st_mtime,
                    "size": stat.st_size,
                }
            )

        # Sort by modification time (newest first)
        file_info.sort(key=lambda f: f["modified"], reverse=True)

        return file_info[:limit]

    def index(self, force: bool = False):
        """Index or reindex the vault."""
        return self.indexer.index_vault(force=force)

    def get_stats(self):
        """Get index statistics."""
        return self.indexer.get_stats()
