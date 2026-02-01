"""
Vault indexer - scans, chunks, and indexes Obsidian vault content.

Optionally extracts reasoning conclusions at index time for enriched search.
"""

from __future__ import annotations

import fnmatch
import hashlib
import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import chromadb
from chromadb.config import Settings

from .chunker import Chunk, ChunkerConfig, MarkdownChunker
from .embedder import EmbedderConfig, OpenAIEmbedder

if TYPE_CHECKING:
    from src.reasoning import ConclusionExtractor, ConclusionStore
    from src.reasoning.extractor import ExtractorConfig

logger = logging.getLogger(__name__)


@dataclass
class IndexerConfig:
    """Configuration for the indexer."""

    vault_path: str
    persist_dir: str = ".chroma"
    collection_name: str = "obsidian_vault"

    # Sub-configs
    chunker_config: ChunkerConfig | None = None
    embedder_config: EmbedderConfig | None = None

    # Reasoning layer (Phase 2)
    reasoning_enabled: bool = False
    extractor_config: ExtractorConfig | None = None

    # Behavior - use field with default_factory for mutable default
    ignore_patterns: list[str] | None = None

    def __post_init__(self):
        if self.ignore_patterns is None:
            self.ignore_patterns = [
                ".obsidian/*",
                ".trash/*",
                ".venv*/*",
                ".git/*",
                "node_modules/*",
                "*.excalidraw.md",
            ]


@dataclass
class IndexStats:
    """Statistics about the index."""

    total_files: int
    total_chunks: int
    indexed_at: datetime
    vault_path: str
    total_conclusions: int = 0
    reasoning_enabled: bool = False

    def to_dict(self) -> dict:
        result = {
            "total_files": self.total_files,
            "total_chunks": self.total_chunks,
            "indexed_at": self.indexed_at.isoformat(),
            "vault_path": self.vault_path,
        }
        if self.reasoning_enabled:
            result["total_conclusions"] = self.total_conclusions
            result["reasoning_enabled"] = True
        return result


class VaultIndexer:
    """
    Indexes an Obsidian vault into ChromaDB for semantic search.

    Features:
    - Scans vault for markdown files
    - Chunks documents intelligently
    - Creates embeddings via OpenAI
    - Stores in ChromaDB with metadata
    - Supports incremental updates (by file hash)
    """

    def __init__(self, config: IndexerConfig, api_key: str | None = None):
        self.config = config
        self.vault_path = Path(config.vault_path).resolve()

        # Validate vault path exists
        if not self.vault_path.exists():
            raise ValueError(f"Vault path does not exist: {self.vault_path}")
        if not self.vault_path.is_dir():
            raise ValueError(f"Vault path is not a directory: {self.vault_path}")

        logger.info(f"Initializing indexer for vault: {self.vault_path}")

        # Initialize components
        self.chunker = MarkdownChunker(config.chunker_config)
        self.embedder = OpenAIEmbedder(api_key=api_key, config=config.embedder_config)

        # Initialize ChromaDB
        persist_path = Path(config.persist_dir).resolve()
        persist_path.mkdir(parents=True, exist_ok=True)

        self.chroma_client = chromadb.PersistentClient(
            path=str(persist_path), settings=Settings(anonymized_telemetry=False)
        )

        # Get or create collection
        self.collection = self.chroma_client.get_or_create_collection(
            name=config.collection_name, metadata={"hnsw:space": "cosine"}
        )

        # Load file hashes for incremental indexing
        self.hash_file = persist_path / "file_hashes.json"
        self.file_hashes = self._load_hashes()

        logger.debug(f"Loaded {len(self.file_hashes)} file hashes from cache")

        # Initialize reasoning layer if enabled
        self.conclusion_extractor: ConclusionExtractor | None = None
        self.conclusion_store: ConclusionStore | None = None

        if config.reasoning_enabled:
            self._init_reasoning(api_key, persist_path)

    def _init_reasoning(self, api_key: str | None, persist_path: Path) -> None:
        """Initialize reasoning layer components."""
        from src.reasoning import ConclusionExtractor, ConclusionStore
        from src.reasoning.extractor import ExtractorConfig

        logger.info("Initializing reasoning layer...")

        extractor_config = self.config.extractor_config or ExtractorConfig()
        self.conclusion_extractor = ConclusionExtractor(
            api_key=api_key,
            config=extractor_config,
        )
        self.conclusion_store = ConclusionStore(
            persist_dir=str(persist_path),
            embedder=self.embedder,
        )

    def _load_hashes(self) -> dict[str, str]:
        """Load previously computed file hashes."""
        if self.hash_file.exists():
            try:
                with open(self.hash_file) as f:
                    return json.load(f)
            except (OSError, json.JSONDecodeError) as e:
                logger.warning(f"Failed to load hash cache: {e}")
                return {}
        return {}

    def _save_hashes(self):
        """Save file hashes for incremental indexing."""
        try:
            with open(self.hash_file, "w") as f:
                json.dump(self.file_hashes, f)
        except OSError as e:
            logger.warning(f"Failed to save hash cache: {e}")

    def _compute_hash(self, content: str) -> str:
        """Compute hash of file content.

        Uses 32 hex chars (128 bits) to avoid birthday paradox collisions
        with large vaults (100k+ files over time).
        """
        return hashlib.sha256(content.encode()).hexdigest()[:32]

    def _should_ignore(self, path: Path) -> bool:
        """Check if a file should be ignored using glob pattern matching."""
        rel_path = str(path.relative_to(self.vault_path))

        if self.config.ignore_patterns is None:
            return False

        for pattern in self.config.ignore_patterns:
            # Use fnmatch for glob-style pattern matching
            if fnmatch.fnmatch(rel_path, pattern):
                return True
            # Also check each path component for directory patterns
            parts = rel_path.split(os.sep)
            for i, part in enumerate(parts):
                # Check if any directory in path matches a directory pattern
                partial_path = os.sep.join(parts[: i + 1])
                if fnmatch.fnmatch(partial_path, pattern.rstrip("/*")):
                    return True
                if fnmatch.fnmatch(part, pattern.rstrip("/*")):
                    return True

        return False

    def scan_vault(self) -> list[Path]:
        """Scan vault for markdown files, skipping symlinks for security."""
        md_files = []

        for path in self.vault_path.rglob("*.md"):
            # Skip symlinks to prevent reading files outside the vault
            if path.is_symlink():
                logger.debug(f"Skipping symlink: {path}")
                continue
            if not self._should_ignore(path):
                md_files.append(path)

        return sorted(md_files)

    def index_vault(self, force: bool = False) -> IndexStats:
        """
        Index the entire vault.

        Args:
            force: If True, reindex all files regardless of hash

        Returns:
            IndexStats with indexing results
        """
        files = self.scan_vault()
        files_indexed = 0

        all_chunks: list[Chunk] = []
        files_to_index: list[tuple[Path, str]] = []

        logger.info(f"Scanning {len(files)} files...")

        # Clean up stale documents (files deleted from vault but still in index)
        current_paths = {str(f.relative_to(self.vault_path)) for f in files}
        stale_paths = set(self.file_hashes.keys()) - current_paths
        if stale_paths:
            logger.info(f"Removing {len(stale_paths)} stale documents from index...")
            for stale_path in stale_paths:
                try:
                    self.collection.delete(where={"source_path": stale_path})
                    # Also remove stale conclusions if reasoning is enabled
                    if self.conclusion_store:
                        self.conclusion_store.delete_by_source(stale_path)
                    del self.file_hashes[stale_path]
                    logger.debug(f"Removed stale: {stale_path}")
                except Exception as e:
                    logger.debug(f"Failed to remove stale {stale_path}: {e}")

        # First pass: determine what needs indexing
        for file_path in files:
            rel_path = str(file_path.relative_to(self.vault_path))
            try:
                content = file_path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as e:
                logger.warning(f"Failed to read {rel_path}: {e}")
                continue

            content_hash = self._compute_hash(content)

            if force or self.file_hashes.get(rel_path) != content_hash:
                files_to_index.append((file_path, content))
                self.file_hashes[rel_path] = content_hash

        if not files_to_index:
            logger.info("No files need indexing.")
            total_conclusions = 0
            if self.conclusion_store:
                total_conclusions = self.conclusion_store.count()
            return IndexStats(
                total_files=len(files),
                total_chunks=self.collection.count(),
                indexed_at=datetime.now(),
                vault_path=str(self.vault_path),
                total_conclusions=total_conclusions,
                reasoning_enabled=self.config.reasoning_enabled,
            )

        logger.info(f"Indexing {len(files_to_index)} files...")

        # Second pass: chunk all files
        for file_path, content in files_to_index:
            rel_path = str(file_path.relative_to(self.vault_path))

            # Remove old chunks for this file
            try:
                self.collection.delete(where={"source_path": rel_path})
            except ValueError:
                # Collection might be empty or have no matching documents
                pass
            except Exception as e:
                # Log but don't fail - old chunks will be overwritten anyway
                logger.debug(f"Failed to delete old chunks for {rel_path}: {e}")

            # Remove old conclusions if reasoning is enabled
            if self.conclusion_store:
                try:
                    self.conclusion_store.delete_by_source(rel_path)
                except Exception as e:
                    logger.debug(f"Failed to delete old conclusions for {rel_path}: {e}")

            # Chunk the document
            chunks = self.chunker.chunk_document(content, rel_path)
            all_chunks.extend(chunks)
            files_indexed += 1

        if not all_chunks:
            logger.info("No chunks generated.")
            return IndexStats(
                total_files=len(files),
                total_chunks=0,
                indexed_at=datetime.now(),
                vault_path=str(self.vault_path),
                total_conclusions=0,
                reasoning_enabled=self.config.reasoning_enabled,
            )

        logger.info(f"Embedding {len(all_chunks)} chunks...")

        # Third pass: embed all chunks
        texts = [chunk.content for chunk in all_chunks]
        embeddings = self.embedder.embed_texts(texts, is_query=False)

        # Fourth pass: store in ChromaDB
        ids = []
        documents = []
        metadatas = []

        for chunk in all_chunks:
            chunk_id = f"{chunk.source_path}:{chunk.chunk_index}"
            ids.append(chunk_id)
            documents.append(chunk.content)
            metadatas.append(
                {
                    "source_path": chunk.source_path,
                    "chunk_index": chunk.chunk_index,
                    "title": chunk.title or "",
                    "heading": chunk.heading or "",
                    "tags": ",".join(chunk.tags),
                    "token_estimate": chunk.token_estimate,
                }
            )

        # Batch insert
        batch_size = 500
        for i in range(0, len(ids), batch_size):
            end = min(i + batch_size, len(ids))
            self.collection.add(
                ids=ids[i:end],
                embeddings=embeddings[i:end],
                documents=documents[i:end],
                metadatas=metadatas[i:end],
            )
            logger.debug(f"Stored batch {i // batch_size + 1}")

        # Save hashes
        self._save_hashes()

        total_chunks = self.collection.count()

        # Fifth pass: extract conclusions if reasoning is enabled
        total_conclusions = 0
        if self.conclusion_extractor and self.conclusion_store:
            total_conclusions = self._extract_conclusions(all_chunks)

        logger.info(
            f"Indexed {files_indexed} files, {len(all_chunks)} chunks. Total: {total_chunks}."
        )
        if total_conclusions:
            logger.info(f"Extracted {total_conclusions} conclusions.")

        return IndexStats(
            total_files=len(files),
            total_chunks=total_chunks,
            indexed_at=datetime.now(),
            vault_path=str(self.vault_path),
            total_conclusions=total_conclusions,
            reasoning_enabled=self.config.reasoning_enabled,
        )

    def _extract_conclusions(self, chunks: list[Chunk]) -> int:
        """
        Extract conclusions from chunks using LLM.

        Args:
            chunks: List of chunks to process

        Returns:
            Number of conclusions extracted
        """
        from src.reasoning.models import ChunkContext

        if not self.conclusion_extractor or not self.conclusion_store:
            return 0

        logger.info(f"Extracting conclusions from {len(chunks)} chunks...")

        all_conclusions = []

        for i, chunk in enumerate(chunks):
            chunk_id = f"{chunk.source_path}:{chunk.chunk_index}"

            # Build context for the extractor
            context = ChunkContext(
                source_path=chunk.source_path,
                title=chunk.title or "",
                heading=chunk.heading,
                tags=chunk.tags,
                chunk_index=chunk.chunk_index,
            )

            try:
                conclusions = self.conclusion_extractor.extract_conclusions(
                    chunk=chunk.content,
                    chunk_id=chunk_id,
                    context=context,
                )
                all_conclusions.extend(conclusions)

                if (i + 1) % 50 == 0:
                    logger.debug(
                        f"Processed {i + 1}/{len(chunks)} chunks, "
                        f"{len(all_conclusions)} conclusions so far"
                    )
            except Exception as e:
                logger.warning(f"Failed to extract conclusions from {chunk_id}: {e}")
                continue

        # Store all conclusions
        if all_conclusions:
            self.conclusion_store.add(all_conclusions)

        return len(all_conclusions)

    def get_stats(self) -> IndexStats:
        """Get current index statistics."""
        total_conclusions = 0
        if self.conclusion_store:
            total_conclusions = self.conclusion_store.count()

        return IndexStats(
            total_files=len(self.scan_vault()),
            total_chunks=self.collection.count(),
            indexed_at=datetime.now(),
            vault_path=str(self.vault_path),
            total_conclusions=total_conclusions,
            reasoning_enabled=self.config.reasoning_enabled,
        )

    def delete_index(self):
        """Delete the entire index."""
        logger.info("Deleting index...")
        self.chroma_client.delete_collection(self.config.collection_name)
        self.collection = self.chroma_client.create_collection(
            name=self.config.collection_name, metadata={"hnsw:space": "cosine"}
        )
        self.file_hashes = {}
        self._save_hashes()

        # Clear conclusions if reasoning is enabled
        if self.conclusion_store:
            self.conclusion_store.clear()
            logger.debug("Cleared conclusion store")

        logger.info("Index deleted.")
