"""
RAG Engine - Query and retrieval for semantic search.

Supports two modes:
1. Basic RAG: Chunk-based semantic search (Phase 1)
2. Reasoning-enhanced: Includes extracted conclusions (Phase 2)
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path

from .indexer import IndexerConfig, VaultIndexer
from .reasoner import Conclusion, Reasoner, ReasonerConfig

logger = logging.getLogger(__name__)


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
    result_type: str = "chunk"  # "chunk" or "conclusion"

    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "source_path": self.source_path,
            "title": self.title,
            "heading": self.heading,
            "tags": self.tags,
            "score": round(self.score, 4),
            "chunk_index": self.chunk_index,
            "result_type": self.result_type,
        }


@dataclass
class ConclusionResult:
    """A conclusion search result."""

    text: str
    conclusion_type: str
    certainty: str
    source_paths: list[str]
    premises: list[dict]
    tags: list[str]
    score: float

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "conclusion_type": self.conclusion_type,
            "certainty": self.certainty,
            "source_paths": self.source_paths,
            "premises": self.premises,
            "tags": self.tags,
            "score": round(self.score, 4),
        }


@dataclass
class SearchResponse:
    """Response from a search query."""

    query: str
    results: list[SearchResult]
    total_chunks_searched: int
    conclusions: list[ConclusionResult] = field(default_factory=list)
    total_conclusions_searched: int = 0

    def to_dict(self) -> dict:
        response = {
            "query": self.query,
            "results": [r.to_dict() for r in self.results],
            "total_chunks_searched": self.total_chunks_searched,
        }
        if self.conclusions:
            response["conclusions"] = [c.to_dict() for c in self.conclusions]
            response["total_conclusions_searched"] = self.total_conclusions_searched
        return response


class RAGEngine:
    """
    Query engine for semantic search over indexed vault.

    Features:
    - Semantic similarity search
    - Tag-based filtering
    - Result ranking and formatting
    - Reasoning layer for conclusion extraction (Phase 2)
    """

    def __init__(
        self,
        vault_path: str,
        persist_dir: str = ".chroma",
        api_key: str | None = None,
        reasoning_enabled: bool = False,
        reasoner_config: ReasonerConfig | None = None,
    ):
        self.vault_path = Path(vault_path).resolve()
        self.reasoning_enabled = reasoning_enabled

        # Initialize indexer (which gives us access to ChromaDB)
        self.indexer = VaultIndexer(
            config=IndexerConfig(
                vault_path=vault_path,
                persist_dir=persist_dir,
            ),
            api_key=api_key,
        )

        # Use the same embedder for queries
        self.embedder = self.indexer.embedder
        self.collection = self.indexer.collection

        # Initialize conclusions collection for Phase 2
        self.conclusions_collection = self.indexer.chroma_client.get_or_create_collection(
            name="conclusions",
            metadata={"description": "Reasoned conclusions from documents"},
        )

        # Initialize reasoner if enabled
        self.reasoner = None
        if reasoning_enabled:
            self.reasoner = Reasoner(
                config=reasoner_config or ReasonerConfig(),
                api_key=api_key,
            )

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
            top_k: Maximum number of results to return
            tags: Optional list of tags to filter by (OR logic)
            min_score: Minimum similarity score (0-1)

        Returns:
            SearchResponse with ranked results
        """
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

    def index(self, force: bool = False, with_reasoning: bool = False):
        """
        Index or reindex the vault.

        Args:
            force: Force full reindex even if unchanged
            with_reasoning: Extract conclusions during indexing (Phase 2)

        Returns:
            IndexStats with indexing results
        """
        stats = self.indexer.index_vault(force=force)

        if with_reasoning and self.reasoner:
            self._index_with_reasoning()

        return stats

    def _index_with_reasoning(self):
        """Extract and store conclusions from indexed chunks."""
        if not self.reasoner:
            logger.warning("Reasoner not initialized, skipping reasoning pass")
            return

        logger.info("Extracting conclusions from indexed chunks...")

        # Get all documents from the collection
        all_docs = self.collection.get(include=["documents", "metadatas"])

        if not all_docs["ids"]:
            logger.info("No documents to reason over")
            return

        # Clear existing conclusions
        try:
            existing = self.conclusions_collection.get()
            if existing["ids"]:
                self.conclusions_collection.delete(ids=existing["ids"])
        except Exception:
            pass

        conclusion_count = 0
        for i, (doc_id, content, metadata) in enumerate(
            zip(all_docs["ids"], all_docs["documents"], all_docs["metadatas"])
        ):
            if not content:
                continue

            tags_str = metadata.get("tags", "")
            tags = [t.strip() for t in tags_str.split(",") if t.strip()]

            conclusions = self.reasoner.extract_conclusions(
                content=content,
                source_path=metadata.get("source_path", ""),
                chunk_index=metadata.get("chunk_index", 0),
                tags=tags,
            )

            for j, conclusion in enumerate(conclusions):
                # Embed the conclusion text
                embedding = self.embedder.embed_text(conclusion.text)

                # Store in conclusions collection
                self.conclusions_collection.add(
                    ids=[f"{doc_id}_conclusion_{j}"],
                    embeddings=[embedding],
                    documents=[conclusion.text],
                    metadatas=[
                        {
                            "conclusion_type": conclusion.conclusion_type.value,
                            "certainty": conclusion.certainty,
                            "source_paths": ",".join(conclusion.source_paths),
                            "tags": ",".join(conclusion.tags),
                            "premises": str(conclusion.to_dict()["premises"]),
                        }
                    ],
                )
                conclusion_count += 1

            if (i + 1) % 10 == 0:
                logger.info(f"Processed {i + 1} chunks, {conclusion_count} conclusions")

        logger.info(f"Reasoning complete: {conclusion_count} conclusions extracted")

    def search_conclusions(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[ConclusionResult]:
        """
        Search extracted conclusions.

        Args:
            query: Natural language query
            top_k: Maximum number of conclusions to return

        Returns:
            List of ConclusionResult objects
        """
        if self.conclusions_collection.count() == 0:
            return []

        query_embedding = self.embedder.embed_text(query)

        results = self.conclusions_collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

        conclusion_results = []
        if results["ids"] and results["ids"][0]:
            for i, doc_id in enumerate(results["ids"][0]):
                distance = results["distances"][0][i]
                score = 1 - distance

                metadata = results["metadatas"][0][i]
                text = results["documents"][0][i]

                # Parse stored data
                source_paths = metadata.get("source_paths", "").split(",")
                tags = [t.strip() for t in metadata.get("tags", "").split(",") if t.strip()]

                # Parse premises (stored as string representation)
                try:
                    import ast
                    premises = ast.literal_eval(metadata.get("premises", "[]"))
                except Exception:
                    premises = []

                conclusion_results.append(
                    ConclusionResult(
                        text=text,
                        conclusion_type=metadata.get("conclusion_type", "unknown"),
                        certainty=metadata.get("certainty", "unknown"),
                        source_paths=source_paths,
                        premises=premises,
                        tags=tags,
                        score=score,
                    )
                )

        return conclusion_results

    def search_with_reasoning(
        self,
        query: str,
        top_k: int = 5,
        include_conclusions: bool = True,
    ) -> SearchResponse:
        """
        Search combining chunks and conclusions.

        Args:
            query: Natural language query
            top_k: Maximum results per type
            include_conclusions: Whether to include conclusions

        Returns:
            SearchResponse with both chunks and conclusions
        """
        # Get chunk results
        response = self.search(query, top_k=top_k)

        # Get conclusion results if enabled
        conclusions = []
        conclusions_count = 0
        if include_conclusions and self.conclusions_collection.count() > 0:
            conclusions = self.search_conclusions(query, top_k=top_k)
            conclusions_count = self.conclusions_collection.count()

        return SearchResponse(
            query=response.query,
            results=response.results,
            total_chunks_searched=response.total_chunks_searched,
            conclusions=conclusions,
            total_conclusions_searched=conclusions_count,
        )

    def get_stats(self):
        """Get index statistics including conclusions."""
        stats = self.indexer.get_stats()
        stats["conclusions_count"] = self.conclusions_collection.count()
        return stats
