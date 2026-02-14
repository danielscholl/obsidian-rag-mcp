# Claude Desktop Integration Guide

Connect the Obsidian RAG MCP server to Claude Desktop (formerly Claude Code).

## Prerequisites

1. [Claude Desktop](https://claude.ai/download) installed
2. Project cloned and dependencies installed:
   ```bash
   git clone https://github.com/ed-insights-ai/obsidian-rag-mcp.git
   cd obsidian-rag-mcp
   uv sync
   ```
3. OpenAI API key

## Configuration

### Linux / macOS

Edit `~/.claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "obsidian-rag": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "/path/to/obsidian-rag-mcp",
        "obsidian-rag", "serve",
        "--vault", "/path/to/your/vault"
      ],
      "env": {
        "OPENAI_API_KEY": "sk-..."
      }
    }
  }
}
```

### Windows

Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "obsidian-rag": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "C:\\path\\to\\obsidian-rag-mcp",
        "obsidian-rag", "serve",
        "--vault", "C:\\path\\to\\your\\vault"
      ],
      "env": {
        "OPENAI_API_KEY": "sk-..."
      }
    }
  }
}
```

**Note:** Use double backslashes (`\\`) in Windows paths within JSON.

### With Reasoning Enabled

Add `--reasoning` to the args:

```json
{
  "mcpServers": {
    "obsidian-rag": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "/path/to/obsidian-rag-mcp",
        "obsidian-rag", "serve",
        "--vault", "/path/to/your/vault",
        "--reasoning"
      ],
      "env": {
        "OPENAI_API_KEY": "sk-..."
      }
    }
  }
}
```

## Restart Claude Desktop

After editing the config, fully restart Claude Desktop for changes to take effect.

## Verify Connection

In Claude Desktop, type `/mcp` to see connected servers. You should see `obsidian-rag` listed.

## Available Tools

| Tool | Description |
|------|-------------|
| `search_vault` | Semantic search across all content |
| `search_by_tag` | Filter by Obsidian tags |
| `get_note` | Retrieve full note content |
| `get_related` | Find similar notes |
| `list_recent` | Recently modified notes |
| `index_status` | Check index statistics |
| `search_with_reasoning` | Search with extracted conclusions |
| `get_conclusion_trace` | Trace reasoning for a conclusion |
| `explore_connected_conclusions` | Find related conclusions |

## Example Prompts

Once connected, try:

- "Search my vault for RCAs about database connection issues"
- "Find notes tagged with #project and #2024"
- "What's related to the kubernetes deployment runbook?"
- "Show me recent changes to my vault"
- "Search for conclusions about authentication failures" (with reasoning enabled)

## Troubleshooting

### Server not appearing

1. Check config file path is correct
2. Verify JSON syntax is valid
3. Restart Claude Desktop completely (quit and reopen)

### "uv not found"

Ensure uv is in your PATH. On Windows, you may need to specify the full path:

```json
{
  "command": "C:\\Users\\YourName\\.local\\bin\\uv.exe",
  ...
}
```

### Connection errors

Check the Claude Desktop logs:
- macOS: `~/Library/Logs/Claude/`
- Windows: `%APPDATA%\Claude\logs\`

### No search results

Index your vault first:

```bash
uv run --directory /path/to/obsidian-rag-mcp obsidian-rag index --vault /path/to/your/vault
```

### Slow first query

The first query loads the ChromaDB index into memory. Subsequent queries are faster.
