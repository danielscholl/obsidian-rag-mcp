# Getting Started

A 5-minute guide to semantic search over your markdown files.

## 1. Install

```bash
git clone https://github.com/ed-insights-ai/obsidian-rag-mcp.git
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

Add to `~/.claude/claude_desktop_config.json` (or `%APPDATA%\Claude\` on Windows):

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

Restart Claude Desktop, then ask:
- "Search my vault for notes about kubernetes"
- "Find RCAs related to authentication"
- "What did I write about the Q3 migration?"

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

- [Claude Desktop Setup](CLAUDE_CODE_SETUP.md) - Full MCP integration guide
- [Integration Guide](INTEGRATION.md) - Use with other agents/pipelines
- [Architecture](ARCHITECTURE.md) - How it works under the hood
