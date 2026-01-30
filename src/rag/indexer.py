"""
Vault indexer - scans, chunks, and indexes Obsidian vault content.
"""

import hashlib
import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import chromadb
from chromadb.config import Settings

from .chunker import Chunk, ChunkerConfig, MarkdownChunker
from .embedder import EmbedderConfig, OpenAIEmbedder

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

    # Behavior - use field with default_factory for mutable default
    ignore_patterns: list[str] | None = None

    def __post_init__(self):
        if self.ignore_patterns is None:
            self.ignore_patterns = [
                ".obsidian/*",
                ".trash/*",
                "*.excalidraw.md",
            ]


@dataclass
class IndexStats:
    """Statistics about the index."""

    total_files: int
    total_chunks: int
    indexed_at: datetime
    vault_path: str

    def to_dict(self) -> dict:
        return {
            "total_files": self.total_files,
            "total_chunks": self.total_chunks,
            "indexed_at": self.indexed_at.isoformat(),
            "vault_path": self.vault_path,
        }


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
        """Compute hash of file content."""
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _should_ignore(self, path: Path) -> bool:
        """Check if a file should be ignored."""
        rel_path = str(path.relative_to(self.vault_path))

        if self.config.ignore_patterns is None:
            return False

        for pattern in self.config.ignore_patterns:
            if pattern.endswith("/*"):
                # Directory pattern
                dir_name = pattern[:-2]
                if rel_path.startswith(dir_name + "/") or rel_path.startswith(
                    dir_name + os.sep
                ):
                    return True
            elif pattern.startswith("*."):
                # Extension pattern
                if rel_path.endswith(pattern[1:]):
                    return True
            elif rel_path == pattern:
                return True

        return False

    def scan_vault(self) -> list[Path]:
        """Scan vault for markdown files."""
        md_files = []

        for path in self.vault_path.rglob("*.md"):
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
            return IndexStats(
                total_files=len(files),
                total_chunks=self.collection.count(),
                indexed_at=datetime.now(),
                vault_path=str(self.vault_path),
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
        logger.info(
            f"Indexed {files_indexed} files, {len(all_chunks)} chunks. Total: {total_chunks}."
        )

        return IndexStats(
            total_files=len(files),
            total_chunks=total_chunks,
            indexed_at=datetime.now(),
            vault_path=str(self.vault_path),
        )

    def get_stats(self) -> IndexStats:
        """Get current index statistics."""
        return IndexStats(
            total_files=len(self.scan_vault()),
            total_chunks=self.collection.count(),
            indexed_at=datetime.now(),
            vault_path=str(self.vault_path),
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
        logger.info("Index deleted.")
