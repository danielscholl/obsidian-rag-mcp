# Development Guide

Get up and running with obsidian-rag-mcp locally.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- OpenAI API key

## Quick Start

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

## Running Tests

```bash
# All tests
uv run pytest

# Specific module
uv run pytest tests/test_engine.py

# With coverage
uv run pytest --cov=src
```

## Code Quality

```bash
# Format
uv run black src/ tests/

# Lint
uv run ruff check src/ tests/

# Type check (optional)
uv run mypy src/ --ignore-missing-imports
```

Pre-commit hooks run automatically on commit.

## MCP Server

### Standalone

```bash
uv run obsidian-rag serve --vault /path/to/vault
```

### With Claude Code

Add to `~/.claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "obsidian-rag": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/obsidian-rag-mcp", "obsidian-rag", "serve"],
      "env": {
        "VAULT_PATH": "/path/to/your/vault",
        "OPENAI_API_KEY": "sk-..."
      }
    }
  }
}
```

Then restart Claude Code.

## Project Structure

```
src/
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

tests/             # pytest tests
vault/             # Sample Obsidian vault for testing
docs/              # Documentation
```

## Reasoning Layer

Enable conclusion extraction with:

```bash
uv run obsidian-rag index --vault ./vault --reasoning
```

Or set `REASONING_ENABLED=true` environment variable.

**Note:** Reasoning requires additional LLM calls and takes longer to index.

## Troubleshooting

### "No module named 'src'"

Run commands with `uv run` from the project root, not plain `python`.

### "OPENAI_API_KEY not set"

```bash
export OPENAI_API_KEY="sk-..."
```

### ChromaDB errors

Delete the `.chroma` directory and re-index:

```bash
rm -rf .chroma
uv run obsidian-rag index --vault ./vault
```

### Empty search results

Make sure you indexed first. Check with:

```bash
uv run obsidian-rag stats --vault ./vault
```
