# Obsidian RAG MCP Server

Semantic search for your Obsidian vault, exposed as an MCP server for Claude Code integration.

## What This Does

Turn your Obsidian vault into a searchable knowledge base that AI assistants can query semantically. Instead of keyword matching, find documents by meaning.

**Example:**
> "Find RCAs where database timeouts caused customer-facing issues"

Returns relevant RCA documents even if they use terms like "CosmosDB latency", "connection pool exhaustion", or "query timeout" — not just exact keyword matches.

## Features

- 🔍 **Semantic Search**: Find documents by meaning, not just keywords
- 🏷️ **Tag-Aware**: Filter searches by Obsidian tags
- 📊 **Metadata Extraction**: Leverages frontmatter and document structure
- 🔌 **MCP Integration**: Works directly with Claude Code
- 🏠 **Local-First**: Your data stays on your machine (only embeddings sent to OpenAI)
- ⚡ **Fast**: Sub-second queries on 100+ document vaults

## Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key (for embeddings)
- An Obsidian vault (or use the included sample vault)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/obsidian-rag-mcp.git
cd obsidian-rag-mcp

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows

# Install dependencies
pip install -e .

# Set up environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Index Your Vault

```bash
# Index the sample vault
obsidian-rag index ./vault

# Or index your own vault
obsidian-rag index /path/to/your/obsidian/vault
```

### Test It

```bash
# Search from CLI
obsidian-rag search "database connection issues"

# Start the MCP server
obsidian-rag serve
```

### Connect to Claude Code

Add to your Claude Code MCP configuration:

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

## MCP Tools

Once connected, Claude Code has access to these tools:

| Tool | Description |
|------|-------------|
| `search_vault` | Semantic search across all vault content |
| `search_by_tag` | Search filtered by Obsidian tags |
| `get_related` | Find notes related to a given note |
| `get_note` | Retrieve full content of a specific note |
| `list_recent` | List recently modified notes |

## Sample Vault

The `vault/` directory contains sample RCA documents for testing. To regenerate:

```bash
python scripts/seed_vault.py
```

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed system design.

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Type checking
mypy src

# Linting
ruff check src
```

## Configuration

Environment variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for embeddings |
| `OBSIDIAN_VAULT_PATH` | No | Default vault path |
| `CHROMA_PERSIST_DIR` | No | ChromaDB storage location |

## Cost

Embedding costs with OpenAI text-embedding-3-small:
- ~100 notes (avg 2000 tokens each): ~$0.02 per full reindex
- Queries: ~$0.00001 per query

## License

MIT

## Acknowledgments

- [ChromaDB](https://www.trychroma.com/) for the vector database
- [MCP](https://modelcontextprotocol.io/) for the protocol spec
- [OpenAI](https://openai.com/) for embeddings
