"""
RAG Engine - Query and retrieval for semantic search.
"""

from dataclasses import dataclass
from pathlib import Path

from .indexer import IndexerConfig, VaultIndexer


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


class RAGEngine:
    """
    Query engine for semantic search over indexed vault.

    Features:
    - Semantic similarity search
    - Tag-based filtering
    - Result ranking and formatting
    """

    def __init__(
        self,
        vault_path: str,
        persist_dir: str = ".chroma",
        api_key: str | None = None,
    ):
        self.vault_path = Path(vault_path).resolve()

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
        filtered_results = [r for r in response.results if r.source_path != path][:top_k]

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
