# Obsidian RAG MCP Server

**Your notes, searchable by meaning.**

An MCP server that gives Claude Code semantic search over your Obsidian vault. Ask questions in natural language, get answers from your own documents.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

---

## The Problem

You have 500 notes in Obsidian. You know you wrote something about database timeouts causing customer issues... somewhere. Ctrl+F won't help when you don't remember the exact words.

## The Solution

This server indexes your vault with vector embeddings. Ask for "RCAs where database timeouts caused customer-facing issues" and get results even if your notes use terms like "CosmosDB latency", "connection pool exhaustion", or "query timeout."

Semantic search. Your data stays local. Sub-second queries.

---

## Quick Start

```bash
# Clone and install
git clone https://github.com/ed-insights-ai/obsidian-rag-mcp.git
cd obsidian-rag-mcp
python -m venv .venv && source .venv/bin/activate
pip install -e .

# Configure
cp .env.example .env
# Add your OPENAI_API_KEY to .env

# Index your vault
obsidian-rag index /path/to/your/vault

# Test it
obsidian-rag search "database connection issues"
```

---

## Connect to Claude Code

Add to your MCP configuration (`~/.config/claude/mcp.json` or similar):

```json
{
  "mcpServers": {
    "obsidian-rag": {
      "command": "obsidian-rag",
      "args": ["serve", "--vault", "/path/to/your/vault"],
      "env": {
        "OPENAI_API_KEY": "your-key-here"
      }
    }
  }
}
```

Then ask Claude things like:
- "Search my vault for notes about Kubernetes deployments"
- "Find RCAs related to authentication failures"
- "What did I write about the Q3 migration?"

---

## MCP Tools

| Tool | What it does |
|------|--------------|
| `search_vault` | Semantic search across all content |
| `search_by_tag` | Filter by Obsidian tags |
| `get_related` | Find notes similar to a given note |
| `get_note` | Retrieve full note content |
| `list_recent` | Recently modified notes |

---

## How It Works

1. **Index**: Scans your vault, chunks markdown intelligently (respecting headers, code blocks), generates embeddings via OpenAI
2. **Store**: Vectors go into ChromaDB (local, no external database needed)
3. **Query**: Your question gets embedded, matched against stored vectors, ranked results returned

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the full system design.

---

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | For generating embeddings |
| `OBSIDIAN_VAULT_PATH` | No | Default vault path |
| `CHROMA_PERSIST_DIR` | No | Where to store the vector database |

**Cost**: ~$0.02 to index 100 notes. Queries are essentially free (~$0.00001 each).

---

## Development

```bash
pip install -e ".[dev]"

# Tests
pytest tests/ -v

# Linting + formatting
black src/ tests/ && ruff check src/ tests/

# Type checking
mypy src
```

Pre-commit hooks enforce these on every commit. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow.

---

## Requirements

- Python 3.11+
- OpenAI API key
- An Obsidian vault (or use `vault/` for testing)

---

## License

MIT
