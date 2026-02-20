# Copilot Instructions — obsidian-rag-mcp

## Project

MCP server providing semantic search over Obsidian vaults using ChromaDB and OpenAI embeddings.

## Code Standards

- Python 3.11+ with strict type hints
- Format: `black` (defaults)
- Lint: `ruff` (E, F, I, N, W, UP rules; 100 char line length)
- Type check: `mypy --strict`
- Test: `pytest` with `pytest-asyncio`; minimum 50% coverage

## Repository Structure

```
obsidian_rag_mcp/
├── rag/          # Core: indexer, chunker, embedder, engine
├── reasoning/    # Conclusion extraction: extractor, store, models
├── mcp/          # MCP server (tools exposed to AI assistants)
├── cli/          # Click CLI (index, search, serve, stats)
└── utils/        # Token counting
tests/            # Mirrors package structure
docs/             # Architecture, development, ADRs
```

## Development Flow

```bash
uv sync                                    # Install deps
uv run pytest                              # Run tests
uv run black obsidian_rag_mcp/ tests/      # Format
uv run ruff check obsidian_rag_mcp/ tests/ # Lint
uv run mypy obsidian_rag_mcp/              # Type check
```

## Architectural Patterns

- Async MCP server with global `RAGEngine` instance
- Pydantic models for structured data
- ChromaDB for local vector storage (no external DB)
- Markdown-aware chunking (respects headers, code blocks, frontmatter)
- Incremental indexing by content hash
- OpenAI / Azure OpenAI embedding support

## Commit Messages

Use Conventional Commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`

## Key Decisions (ADRs)

- ADR-0001: ChromaDB as vector store (local-first, embedded)
- ADR-0002: CI health checks (black, ruff, bandit, pip-audit)
- ADR-0003: OpenAI embeddings (text-embedding-3-small)
- ADR-0004: Reasoning layer design (conclusion extraction)

## Common Tasks

### Adding a new MCP tool
1. Define the tool in `obsidian_rag_mcp/mcp/server.py`
2. Add handler logic
3. Add tests in `tests/`
4. Update ARCHITECTURE.md tool table

### Modifying the RAG pipeline
1. Changes go in `obsidian_rag_mcp/rag/`
2. `chunker.py` for parsing, `embedder.py` for embeddings, `engine.py` for queries
3. Keep incremental indexing compatible

### Adding tests
1. Mirror the package structure in `tests/`
2. Use fixtures from `tests/conftest.py`
3. Mock external services (OpenAI, ChromaDB)
