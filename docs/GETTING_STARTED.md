# Getting Started

A 5-minute guide to semantic search over your markdown files.

## 1. Install

```bash
git clone https://github.com/danielscholl/obsidian-rag-mcp.git
cd obsidian-rag-mcp
uv sync
```

**Windows PowerShell:**
```powershell
# Install uv first if needed
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## 2. Set API Key

```bash
# Linux/macOS
export OPENAI_API_KEY="sk-..."

# Windows PowerShell
$env:OPENAI_API_KEY = "sk-..."
```

**Azure OpenAI alternative:**
```bash
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_API_KEY="your-key"
```

## 3. Index Your Vault

```bash
uv run obsidian-rag index /path/to/your/vault
```

This scans all `.md` files, chunks them intelligently, and creates embeddings.

**Output:**
```
Indexing vault: /path/to/your/vault
Index complete:
  Files: 132
  Chunks: 1154
```

## 4. Search

```bash
uv run obsidian-rag search "database connection issues" --vault /path/to/your/vault
```

**Output:**
```
Query: database connection issues
Found 3 results (searched 1154 chunks)

--- Result 1 (score: 0.48) ---
Source: RCAs/2025-05-17-database-connection-pool-exhaustion.md
Tags: database, p1, rca

# 2025-05-17 - Database Connection Pool Exhaustion...
```

## 5. Filter by Tags

```bash
uv run obsidian-rag search "issues" --vault /path/to/vault --tags p1
```

Only returns results with the `#p1` tag.

## 6. Check Stats

```bash
uv run obsidian-rag stats --vault /path/to/your/vault
```

## Optional: Enable Reasoning

Extract conclusions from your notes for richer search:

```bash
# Set env var before indexing
export REASONING_ENABLED=true
uv run obsidian-rag index /path/to/your/vault
```

This uses an LLM to extract logical conclusions from your content.

---

## Connect to Claude Desktop

Add to your MCP config file:
- **Linux/macOS:** `~/.claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

### Linux / macOS

```json
{
  "mcpServers": {
    "obsidian-rag": {
      "command": "uv",
      "args": [
        "run", "--directory", "/path/to/obsidian-rag-mcp",
        "obsidian-rag", "serve", "--vault", "/path/to/your/vault"
      ],
      "env": {
        "OPENAI_API_KEY": "sk-..."
      }
    }
  }
}
```

### Windows

```json
{
  "mcpServers": {
    "obsidian-rag": {
      "command": "uv",
      "args": [
        "run", "--directory", "C:\\path\\to\\obsidian-rag-mcp",
        "obsidian-rag", "serve", "--vault", "C:\\path\\to\\your\\vault"
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

Add `"REASONING_ENABLED": "true"` to the `env` block.

### Verify Connection

Restart Claude Desktop, then type `/mcp` to see connected servers. You should see `obsidian-rag` listed.

Try asking:
- "Search my vault for RCAs about database connection issues"
- "Find notes tagged with #project and #2024"
- "What's related to the kubernetes deployment runbook?"
- "Search for conclusions about authentication failures" (with reasoning enabled)

### Troubleshooting

**Server not appearing:** Check config file path, verify JSON syntax, restart Claude Desktop completely.

**"uv not found":** Ensure uv is in your PATH. On Windows, specify the full path:
```json
{ "command": "C:\\Users\\YourName\\.local\\bin\\uv.exe" }
```

**Connection errors:** Check logs at `~/Library/Logs/Claude/` (macOS) or `%APPDATA%\Claude\logs\` (Windows).

**No search results:** Index your vault first with `uv run obsidian-rag index --vault /path/to/vault`.

**Slow first query:** The first query loads the ChromaDB index into memory. Subsequent queries are faster.

---

## Quick Reference

| Command | What it does |
|---------|--------------|
| `obsidian-rag index <vault>` | Index/reindex vault |
| `obsidian-rag search "query" --vault <path>` | Semantic search |
| `obsidian-rag search "query" --vault <path> --tags tag1` | Filter by tag |
| `obsidian-rag stats --vault <path>` | Show index stats |
| `obsidian-rag serve --vault <path>` | Start MCP server |

---

## Next Steps

- [Integration Guide](INTEGRATION.md) - Use with other agents/pipelines
- [Architecture](ARCHITECTURE.md) - How it works under the hood
- [Development](DEVELOPMENT.md) - Contribute to the project
