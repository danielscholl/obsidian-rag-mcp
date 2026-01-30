# Claude Code Integration Guide

This guide shows how to connect the Obsidian RAG MCP server to Claude Code.

## Prerequisites

1. Clone and set up the project:
   ```bash
   cd ~/projects/obsidian-rag-mcp
   python3.12 -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

2. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=sk-your-key-here
   ```

3. Index your vault:
   ```bash
   PYTHONPATH=. python -c "
   from src.rag import RAGEngine
   engine = RAGEngine(vault_path='./vault')
   engine.index()
   "
   ```

## Claude Code Configuration

Add this to your Claude Code MCP settings:

### Option 1: Stdio Transport (Recommended)

```json
{
  "mcpServers": {
    "obsidian-rag": {
      "command": "/Users/lume/projects/obsidian-rag-mcp/.venv/bin/python",
      "args": [
        "-m", "src.mcp.server"
      ],
      "cwd": "/Users/lume/projects/obsidian-rag-mcp",
      "env": {
        "OPENAI_API_KEY": "your-key-here",
        "OBSIDIAN_VAULT_PATH": "/Users/lume/projects/obsidian-rag-mcp/vault",
        "PYTHONPATH": "/Users/lume/projects/obsidian-rag-mcp"
      }
    }
  }
}
```

### Option 2: Using a shell wrapper

Create `~/projects/obsidian-rag-mcp/run-server.sh`:
```bash
#!/bin/bash
cd /Users/lume/projects/obsidian-rag-mcp
source .venv/bin/activate
export OPENAI_API_KEY="your-key-here"
export OBSIDIAN_VAULT_PATH="./vault"
PYTHONPATH=. python -m src.mcp.server
```

Then in MCP config:
```json
{
  "mcpServers": {
    "obsidian-rag": {
      "command": "/Users/lume/projects/obsidian-rag-mcp/run-server.sh"
    }
  }
}
```

## Available Tools

Once connected, Claude Code has access to:

| Tool | Description | Example Use |
|------|-------------|-------------|
| `search_vault` | Semantic search | "Find RCAs about database timeouts" |
| `search_by_tag` | Tag-filtered search | "Find all P1 incidents" |
| `get_note` | Read full note | "Read the billing-api runbook" |
| `get_related` | Find similar notes | "What's related to this RCA?" |
| `list_recent` | Recent changes | "Show recently modified docs" |
| `index_status` | Check index | "How many docs are indexed?" |

## Testing the Connection

In Claude Code:
```
/mcp
```

You should see `obsidian-rag` in the list of connected servers.

## Example Queries

Once connected, try:

> "Search my vault for past incidents involving CosmosDB connection issues"

> "Find RCAs similar to this kubernetes pod crash we're seeing"

> "What does our runbook say about handling billing-api memory issues?"

> "List the most recent RCA documents"

## Troubleshooting

### Server not starting
- Check Python path: `.venv/bin/python` should exist
- Verify OPENAI_API_KEY is set
- Check vault path exists

### No results
- Run `index_status` to verify the index is populated
- Re-index if needed: `engine.index(force=True)`

### Slow queries
- First query may be slow (loading models)
- Subsequent queries should be <500ms
