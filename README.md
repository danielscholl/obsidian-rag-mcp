# Obsidian RAG MCP Server

**Your notes, searchable by meaning.**

An MCP server that gives Claude Code semantic search over your Obsidian vault. Ask questions in natural language, get answers from your own documents.

[![CI](https://github.com/danielscholl/obsidian-rag-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/danielscholl/obsidian-rag-mcp/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-compatible-green.svg)](https://modelcontextprotocol.io)

---

## The Problem

You have 500 notes in Obsidian. You know you wrote something about database timeouts causing customer issues... somewhere. Ctrl+F won't help when you don't remember the exact words.

## The Solution

This server indexes your vault with vector embeddings. Ask for "RCAs where database timeouts caused customer-facing issues" and get results even if your notes use terms like "CosmosDB latency", "connection pool exhaustion", or "query timeout."

Semantic search. Your data stays local. Sub-second queries.

---

## Quick Start

```bash
# Clone and install (using uv - recommended)
git clone https://github.com/danielscholl/obsidian-rag-mcp.git
cd obsidian-rag-mcp
uv sync

# Set your API key
export OPENAI_API_KEY="sk-..."

# Index the sample vault (or your own)
uv run obsidian-rag index --vault ./vault

# Search it
uv run obsidian-rag search "database connection issues" --vault ./vault
```

<details>
<summary>Output</summary>

```
Query: database connection issues
Found 3 results (searched 1154 chunks)

--- Result 1 (score: 0.480) ---
Source: RCAs/2025-05-17-database-connection-pool-exhaustion.md
Tags: database, p1, rca

# 2025-05-17 - Database Connection Pool Exhaustion in payment-gateway...

--- Result 2 (score: 0.466) ---
Source: RCAs/2025-06-18-database-connection-pool-exhaustion.md
Tags: database, p2, rca

# 2025-06-18 - Database Connection Pool Exhaustion in auth-service...
```

</details>

---

## Connect to Claude Code

Add to `~/.claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "obsidian-rag": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/obsidian-rag-mcp", "obsidian-rag", "serve"],
      "env": {
        "OBSIDIAN_VAULT_PATH": "/path/to/your/vault",
        "OPENAI_API_KEY": "sk-..."
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
| `search_with_reasoning` | Search with extracted conclusions (Phase 2) |

---

## How It Works

1. **Index**: Scans your vault, chunks markdown intelligently (respecting headers, code blocks), generates embeddings via OpenAI
2. **Store**: Vectors go into ChromaDB (local, no external database needed)
3. **Query**: Your question gets embedded, matched against stored vectors, ranked results returned
4. **Reasoning** (optional): Extract conclusions from notes at index time for richer search results

**Documentation:**
- **[Getting Started](docs/GETTING_STARTED.md)** - 5-minute tutorial
- [Architecture](docs/ARCHITECTURE.md) - System design
- [Development](docs/DEVELOPMENT.md) - Local setup (includes Windows)
- [Claude Desktop](docs/CLAUDE_CODE_SETUP.md) - MCP integration
- [Integration](docs/INTEGRATION.md) - Use with other agents/pipelines

---

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes* | For embeddings (and reasoning if enabled) |
| `AZURE_OPENAI_ENDPOINT` | No* | Azure OpenAI endpoint URL |
| `AZURE_API_KEY` | No* | Azure OpenAI API key |
| `AZURE_OPENAI_VERSION` | No | Azure API version (default: `2024-10-21`) |
| `AZURE_EMBEDDING_DEPLOYMENT` | No | Azure deployment name (default: `text-embedding-3-small`) |
| `OBSIDIAN_VAULT_PATH` | No | Default vault path |
| `REASONING_ENABLED` | No | Enable conclusion extraction (default: false) |

\* Either `OPENAI_API_KEY` **or** `AZURE_OPENAI_ENDPOINT` + `AZURE_API_KEY` is required. When both Azure variables are set, Azure OpenAI is used automatically.

**Cost**: ~$0.02 to index 100 notes. Queries are essentially free.

---

## Development

```bash
uv sync

# Tests
uv run pytest

# Lint + format
uv run black obsidian_rag_mcp/ tests/
uv run ruff check obsidian_rag_mcp/ tests/
```

See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for the full guide.

---

## Requirements

- Python 3.11+
- OpenAI API key
- An Obsidian vault (or use `vault/` for testing)

---

## License

MIT

---

<div align="center">

[Getting Started](docs/GETTING_STARTED.md) | [Architecture](docs/ARCHITECTURE.md) | [Development](docs/DEVELOPMENT.md) | [Claude Desktop](docs/CLAUDE_CODE_SETUP.md) | [Integration](docs/INTEGRATION.md)

</div>
