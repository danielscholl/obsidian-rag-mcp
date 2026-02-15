# Development Guide

Get up and running with obsidian-rag-mcp locally.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- OpenAI API key

## Quick Start

### Linux / macOS

```bash
# Clone
git clone https://github.com/ed-insights-ai/obsidian-rag-mcp.git
cd obsidian-rag-mcp

# Install dependencies
uv sync

# Set API key
export OPENAI_API_KEY="sk-..."

# Index sample vault
uv run obsidian-rag index --vault ./vault

# Search
uv run obsidian-rag search "database issues" --vault ./vault
```

### Windows (PowerShell)

```powershell
# Clone
git clone https://github.com/ed-insights-ai/obsidian-rag-mcp.git
cd obsidian-rag-mcp

# Install uv if needed
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Install dependencies
uv sync

# Set API key
$env:OPENAI_API_KEY = "sk-..."

# Index sample vault
uv run obsidian-rag index --vault .\vault

# Search
uv run obsidian-rag search "database issues" --vault .\vault
```

### Windows (CMD)

```cmd
:: Clone
git clone https://github.com/ed-insights-ai/obsidian-rag-mcp.git
cd obsidian-rag-mcp

:: Install dependencies
uv sync

:: Set API key
set OPENAI_API_KEY=sk-...

:: Index sample vault
uv run obsidian-rag index --vault .\vault

:: Search
uv run obsidian-rag search "database issues" --vault .\vault
```

## Running Tests

```bash
# All tests (88 passing)
uv run pytest

# Specific module
uv run pytest tests/test_engine.py

# With coverage
uv run pytest --cov=obsidian_rag_mcp
```

## Code Quality

```bash
# Format
uv run black obsidian_rag_mcp/ tests/

# Lint
uv run ruff check obsidian_rag_mcp/ tests/

# Type check (optional)
uv run mypy obsidian_rag_mcp/ --ignore-missing-imports
```

Pre-commit hooks run automatically on commit.

## MCP Server

### Standalone

```bash
uv run obsidian-rag serve --vault /path/to/vault
```

### With Claude Desktop

See [CLAUDE_CODE_SETUP.md](CLAUDE_CODE_SETUP.md) for full instructions.

## Project Structure

```
obsidian_rag_mcp/
├── mcp/           # MCP server + tools
│   └── server.py  # Tool definitions and handlers
├── rag/           # Core RAG functionality
│   ├── chunker.py # Markdown chunking
│   ├── embedder.py# OpenAI embeddings
│   ├── engine.py  # Search + retrieval
│   └── indexer.py # Vault indexing
└── reasoning/     # Conclusion extraction (Phase 2)
    ├── extractor.py      # LLM-based extraction
    ├── conclusion_store.py # ChromaDB storage
    └── models.py         # Data models

tests/             # pytest tests (88 tests)
vault/             # Sample Obsidian vault for testing
docs/              # Documentation
```

## Reasoning Layer

Enable conclusion extraction with:

```bash
uv run obsidian-rag index --vault ./vault --reasoning
```

Or set environment variable:
- Linux/macOS: `export REASONING_ENABLED=true`
- Windows PowerShell: `$env:REASONING_ENABLED = "true"`
- Windows CMD: `set REASONING_ENABLED=true`

**Note:** Reasoning requires additional LLM calls and takes longer to index.

## Troubleshooting

### "No module named 'obsidian_rag_mcp'"

Run commands with `uv run` from the project root, or install the package with `uv pip install -e .`.

### "OPENAI_API_KEY not set"

Set the environment variable for your platform (see Quick Start above).

### ChromaDB errors

Delete the `.vault` directory and re-index:

```bash
# Linux/macOS
rm -rf .vault

# Windows PowerShell
Remove-Item -Recurse -Force .vault

# Windows CMD
rmdir /s /q .vault
```

Then re-index:
```bash
uv run obsidian-rag index --vault ./vault
```

### Empty search results

Make sure you indexed first:

```bash
uv run obsidian-rag stats --vault ./vault
```

### Windows: "uv not found"

Install uv:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then restart your terminal.
