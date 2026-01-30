---
status: accepted
date: 2026-01-29
---

# Use ChromaDB for Vector Storage

## Context

We need a vector database to store and query document embeddings for semantic search. The system must work locally without requiring external infrastructure, while supporting vaults up to a few thousand documents.

## Decision Drivers

- **Local-first**: No external database dependencies; runs on developer machines
- **Simplicity**: Minimal configuration and operational overhead
- **Python ecosystem**: Native Python API, easy integration
- **Scale**: Sufficient for personal/team vaults (hundreds to low thousands of documents)

## Considered Options

1. **ChromaDB** — Embedded vector database, Python-native
2. **Pinecone** — Cloud-hosted, managed service
3. **Qdrant** — Self-hosted or cloud, more features
4. **pgvector** — Postgres extension, requires Postgres
5. **FAISS** — Facebook's library, lower-level API

## Decision

**ChromaDB** — It's embedded (no separate server), has a clean Python API, persists to disk, and handles our scale requirements without complexity.

## Consequences

**Good:**
- Zero infrastructure setup — just `pip install`
- Persistent storage to local directory
- Simple API for CRUD and similarity search
- Good enough performance for <10k documents

**Bad:**
- Not suitable for massive scale (millions of vectors)
- Limited query features compared to Qdrant/Pinecone
- Single-node only (no distributed queries)

**Acceptable because:**
- Target use case is personal/team vaults, not enterprise scale
- Can migrate to Qdrant/Pinecone later if needed — interface is abstracted

## Notes

If scale requirements change significantly, revisit this decision. The RAG engine interface is designed to allow swapping storage backends.
