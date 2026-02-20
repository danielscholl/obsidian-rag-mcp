# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) documenting significant technical decisions in the project.

## What's an ADR?

An ADR captures *why* we made a particular choice, not just *what* we built. When future contributors ask "why ChromaDB instead of Pinecone?", the answer lives here.

## Format

Each ADR includes:
- **Status**: proposed, accepted, deprecated, superseded
- **Context**: The problem or situation
- **Decision Drivers**: What mattered most
- **Options Considered**: Alternatives we evaluated
- **Decision**: What we chose and why
- **Consequences**: Trade-offs, both good and bad

## Index

| ADR | Title | Status |
|-----|-------|--------|
| [0001](0001-chromadb.md) | Use ChromaDB for Vector Storage | Accepted |
| [0002](0002-ci-health-checks.md) | CI Health Checks as Quality Gates | Accepted |
| [0003](0003-openai-embeddings.md) | Use OpenAI Embeddings for Semantic Search | Accepted |
| [0004](adr-0004-memory-as-reasoning.md) | Memory as Reasoning | Proposed |

## Adding a New ADR

1. Copy an existing ADR as a template
2. Number sequentially (0004, 0005, ...)
3. Fill in all sections honestly — include the bad consequences too
4. Submit via PR for team review
