# CLAUDE.md — Project Context for AI Assistants

## Project Overview

**obsidian-rag-mcp** is an MCP server that provides semantic search over Obsidian vaults. It indexes markdown files with vector embeddings (OpenAI) stored in ChromaDB, then exposes search via the Model Context Protocol for Claude Code and other AI assistants.

## Quick Commands

```bash
# Install
uv sync

# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_engine.py -v

# Format
uv run black obsidian_rag_mcp/ tests/

# Lint
uv run ruff check obsidian_rag_mcp/ tests/

# Type check
uv run mypy obsidian_rag_mcp/

# Security scan
uv run bandit -r obsidian_rag_mcp/ -ll -x tests/

# Dependency audit
pip-audit

# Run all quality checks (CI simulation)
uv run black --check obsidian_rag_mcp/ tests/ && \
uv run ruff check obsidian_rag_mcp/ tests/ && \
uv run mypy obsidian_rag_mcp/ && \
uv run pytest --cov=obsidian_rag_mcp --cov-fail-under=50

# Index sample vault
uv run obsidian-rag index --vault ./vault

# Search
uv run obsidian-rag search "query" --vault ./vault

# Start MCP server
uv run obsidian-rag serve --vault ./vault
```

## Architecture

```
obsidian_rag_mcp/
├── rag/                 # Core RAG pipeline
│   ├── indexer.py       # Vault scanning, chunking, embedding
│   ├── chunker.py       # Markdown-aware chunking (headers, code blocks, frontmatter)
│   ├── embedder.py      # OpenAI / Azure OpenAI embeddings
│   └── engine.py        # Semantic search engine (query interface)
├── reasoning/           # Conclusion extraction layer
│   ├── extractor.py     # LLM-based conclusion extraction
│   ├── conclusion_store.py  # ChromaDB storage for conclusions
│   └── models.py        # Conclusion, ConclusionType dataclasses
├── mcp/
│   ├── server.py        # MCP server (tools: search_vault, search_by_tag, etc.)
│   └── __main__.py      # Entry point
├── cli/
│   └── main.py          # Click CLI (index, search, serve, stats)
└── utils/
    └── tokens.py        # Token counting utilities
```

### Key Patterns

- **Async everywhere**: MCP server is async; engine queries use asyncio
- **Global engine instance**: `server.py` initializes a single `RAGEngine` on startup
- **Pydantic models**: Used for structured data (reasoning models)
- **Click CLI**: Commands in `cli/main.py`
- **ChromaDB local**: Vectors stored locally in `.chroma/` directory
- **Incremental indexing**: Only re-indexes changed files (content hash)

### MCP Tools

| Tool | Description |
|------|-------------|
| `search_vault` | Semantic search across all content |
| `search_by_tag` | Filter by Obsidian tags |
| `get_note` | Retrieve full note content |
| `get_related` | Find similar notes |
| `list_recent` | Recently modified notes |
| `index_status` | Index statistics |
| `search_with_reasoning` | Search with extracted conclusions |

## Code Style

- **Formatter**: `black` (default settings)
- **Linter**: `ruff` (rules: E, F, I, N, W, UP; line-length 100)
- **Type checker**: `mypy --strict`
- **Type hints**: Required for all public functions
- **Docstrings**: Module-level and public functions
- **Imports**: Sorted by ruff (isort-compatible)

## Testing

- Framework: `pytest` with `pytest-asyncio`
- Coverage minimum: 50% (enforced in CI)
- Tests in `tests/` mirror the package structure
- Use existing fixtures in `tests/conftest.py`
- Mock external services (OpenAI, ChromaDB) in unit tests

## Commit Conventions

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new search filter
fix: handle empty vault during indexing
docs: update architecture diagram
refactor(rag): simplify chunker logic
test: add embedder unit tests
chore(ci): add CodeQL scanning
```

Breaking changes: `feat!: require Python 3.12+`

## Dependencies

- **Runtime**: chromadb, openai, mcp, click, pydantic, python-frontmatter, tenacity, tiktoken, python-dotenv
- **Dev**: pytest, pytest-asyncio, pytest-cov, mypy, ruff, black
- **Build**: hatchling
- **Python**: >=3.11, <3.14

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes* | OpenAI API key for embeddings |
| `AZURE_OPENAI_ENDPOINT` | No* | Azure OpenAI endpoint |
| `AZURE_API_KEY` | No* | Azure OpenAI key |
| `VAULT_PATH` | No | Default vault path |
| `REASONING_ENABLED` | No | Enable conclusion extraction |

\* Either OpenAI or Azure OpenAI credentials required.

## Key Documentation

- [Architecture](docs/ARCHITECTURE.md) -- System design and data flow
- [Development](docs/DEVELOPMENT.md) -- Local setup (includes Windows)
- [Getting Started](docs/GETTING_STARTED.md) -- 5-minute tutorial
- [ADRs](docs/decisions/) -- Architectural decision records
