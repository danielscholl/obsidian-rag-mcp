"""
Storage layer for conclusions using ChromaDB.

Provides persistent storage and semantic search over extracted conclusions.
"""

import json
import logging
from pathlib import Path

import chromadb
from chromadb.config import Settings

from .models import Conclusion, ConclusionType, ChunkContext

logger = logging.getLogger(__name__)


class ConclusionStore:
    """
    Persistent storage for conclusions with semantic search.
    
    Uses a separate ChromaDB collection for conclusions, enabling:
    - Fast retrieval by conclusion ID
    - Semantic search over conclusion statements
    - Filtering by type, source, confidence
    """
    
    COLLECTION_NAME = "conclusions"
    
    def __init__(
        self,
        persist_dir: str = ".chroma",
        embedder=None,  # OpenAIEmbedder instance
    ):
        self.persist_dir = Path(persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        
        self.client = chromadb.PersistentClient(
            path=str(self.persist_dir),
            settings=Settings(anonymized_telemetry=False),
        )
        
        self.embedder = embedder
        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            metadata={"description": "Extracted conclusions from vault content"},
        )
        
        logger.debug(f"Initialized conclusion store at {persist_dir}")
    
    def add(self, conclusions: list[Conclusion]) -> int:
        """
        Add conclusions to the store.
        
        Args:
            conclusions: List of conclusions to store
            
        Returns:
            Number of conclusions added
        """
        if not conclusions:
            return 0
        
        ids = []
        documents = []
        metadatas = []
        embeddings = []
        
        for conclusion in conclusions:
            ids.append(conclusion.id)
            documents.append(conclusion.statement)
            metadatas.append({
                "type": conclusion.type.value,
                "confidence": conclusion.confidence,
                "source_chunk_id": conclusion.source_chunk_id,
                "source_path": conclusion.context.source_path,
                "title": conclusion.context.title,
                "heading": conclusion.context.heading or "",
                "tags": ",".join(conclusion.context.tags),
                "chunk_index": conclusion.context.chunk_index,
                "evidence": json.dumps(conclusion.evidence),
                "related_conclusions": ",".join(conclusion.related_conclusions),
                "created_at": conclusion.created_at or "",
            })
        
        # Generate embeddings if embedder provided
        if self.embedder:
            embeddings = self.embedder.embed_texts(documents, is_query=False)
            self.collection.upsert(
                ids=ids,
                documents=documents,
                metadatas=metadatas,
                embeddings=embeddings,
            )
        else:
            self.collection.upsert(
                ids=ids,
                documents=documents,
                metadatas=metadatas,
            )
        
        logger.debug(f"Added {len(conclusions)} conclusions to store")
        return len(conclusions)
    
    def get(self, conclusion_id: str) -> Conclusion | None:
        """Get a conclusion by ID."""
        try:
            result = self.collection.get(
                ids=[conclusion_id],
                include=["documents", "metadatas"],
            )
            
            if not result["ids"]:
                return None
            
            return self._result_to_conclusion(
                result["ids"][0],
                result["documents"][0],
                result["metadatas"][0],
            )
        except Exception as e:
            logger.error(f"Error getting conclusion {conclusion_id}: {e}")
            return None
    
    def search(
        self,
        query: str,
        top_k: int = 10,
        conclusion_type: ConclusionType | None = None,
        min_confidence: float = 0.0,
        source_path: str | None = None,
    ) -> list[Conclusion]:
        """
        Search conclusions semantically.
        
        Args:
            query: Search query
            top_k: Maximum results to return
            conclusion_type: Filter by type
            min_confidence: Minimum confidence threshold
            source_path: Filter by source file
            
        Returns:
            List of matching conclusions
        """
        # Build where clause
        where = {}
        if conclusion_type:
            where["type"] = conclusion_type.value
        if source_path:
            where["source_path"] = source_path
        
        # Query with embedding if available
        if self.embedder:
            query_embedding = self.embedder.embed_text(query)
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k * 2,  # Get extra for filtering
                where=where if where else None,
                include=["documents", "metadatas", "distances"],
            )
        else:
            # Fall back to text search
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k * 2,
                where=where if where else None,
                include=["documents", "metadatas", "distances"],
            )
        
        conclusions = []
        if results["ids"] and results["ids"][0]:
            for i, cid in enumerate(results["ids"][0]):
                metadata = results["metadatas"][0][i]
                
                # Filter by confidence
                if metadata["confidence"] < min_confidence:
                    continue
                
                conclusion = self._result_to_conclusion(
                    cid,
                    results["documents"][0][i],
                    metadata,
                )
                conclusions.append(conclusion)
                
                if len(conclusions) >= top_k:
                    break
        
        return conclusions
    
    def get_by_source(self, source_path: str) -> list[Conclusion]:
        """Get all conclusions from a source file."""
        results = self.collection.get(
            where={"source_path": source_path},
            include=["documents", "metadatas"],
        )
        
        conclusions = []
        if results["ids"]:
            for i, cid in enumerate(results["ids"]):
                conclusions.append(self._result_to_conclusion(
                    cid,
                    results["documents"][i],
                    results["metadatas"][i],
                ))
        
        return conclusions
    
    def delete_by_source(self, source_path: str) -> int:
        """Delete all conclusions from a source file."""
        # Get IDs first
        results = self.collection.get(
            where={"source_path": source_path},
        )
        
        if not results["ids"]:
            return 0
        
        self.collection.delete(ids=results["ids"])
        return len(results["ids"])
    
    def count(self) -> int:
        """Get total number of conclusions."""
        return self.collection.count()
    
    def clear(self) -> None:
        """Delete all conclusions."""
        # Recreate collection
        self.client.delete_collection(self.COLLECTION_NAME)
        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            metadata={"description": "Extracted conclusions from vault content"},
        )
    
    def _result_to_conclusion(
        self,
        cid: str,
        document: str,
        metadata: dict,
    ) -> Conclusion:
        """Convert a ChromaDB result to a Conclusion object."""
        # Parse tags
        tags_str = metadata.get("tags", "")
        tags = [t.strip() for t in tags_str.split(",") if t.strip()]
        
        # Parse evidence
        evidence_str = metadata.get("evidence", "[]")
        try:
            evidence = json.loads(evidence_str)
        except json.JSONDecodeError:
            evidence = []
        
        # Parse related conclusions
        related_str = metadata.get("related_conclusions", "")
        related = [r.strip() for r in related_str.split(",") if r.strip()]
        
        return Conclusion(
            id=cid,
            type=ConclusionType(metadata["type"]),
            statement=document,
            confidence=metadata["confidence"],
            evidence=evidence,
            source_chunk_id=metadata["source_chunk_id"],
            context=ChunkContext(
                source_path=metadata["source_path"],
                title=metadata.get("title", ""),
                heading=metadata.get("heading") or None,
                tags=tags,
                chunk_index=metadata.get("chunk_index", 0),
            ),
            related_conclusions=related,
            created_at=metadata.get("created_at") or None,
        )
