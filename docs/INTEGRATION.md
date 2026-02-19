# Integration Guide

Use obsidian-rag-mcp as a backend for other applications and agents.

## Overview

This project works with any markdown-based knowledge store. While designed for Obsidian vaults, it works with any folder of `.md` files. This makes it ideal for integration with:

- Daily dumps from email/chat/calendar
- Automated note collection agents
- Documentation aggregators
- Knowledge base pipelines

## Architecture for Integration

```
┌─────────────────────┐
│  Your Agent         │
│  (email/chat dump)  │
└─────────┬───────────┘
          │ writes .md files
          ▼
┌─────────────────────┐
│  Vault Directory    │
│  (markdown files)   │
└─────────┬───────────┘
          │ indexed by
          ▼
┌─────────────────────┐
│  obsidian-rag-mcp   │
│  (semantic search)  │
└─────────┬───────────┘
          │ MCP protocol
          ▼
┌─────────────────────┐
│  Claude / LLM       │
│  (queries vault)    │
└─────────────────────┘
```

## Vault Structure Recommendations

For best results with automated dumps:

```
vault/
├── daily/
│   ├── 2024-02-14.md      # Daily summary
│   ├── 2024-02-13.md
│   └── ...
├── emails/
│   ├── 2024-02-14-inbox.md
│   └── ...
├── meetings/
│   ├── 2024-02-14-standup.md
│   └── ...
├── projects/
│   ├── project-alpha.md
│   └── ...
└── chats/
    ├── slack-2024-02-14.md
    └── ...
```

## Markdown Format

The indexer extracts:
- **Title**: First `# heading` or filename
- **Tags**: `#tag` anywhere in content, or YAML frontmatter `tags: [a, b]`
- **Sections**: Split on `## headings` for granular search

### Recommended Template

```markdown
---
date: 2024-02-14
source: email
tags: [inbox, work]
---

# Email Summary - February 14, 2024

## Important Messages

### From: Alice about Project Alpha
Content here...

## Action Items

- [ ] Review PR #123
- [ ] Schedule follow-up

## Notes

Additional context...
```

## Programmatic Usage

### Python API

```python
from obsidian_rag_mcp.rag.engine import RAGEngine

# Initialize
engine = RAGEngine(
    vault_path="/path/to/vault",
    persist_dir="/path/to/chromadb",
    reasoning_enabled=True,  # Optional: extract conclusions
)

# Index (call after adding new files)
stats = engine.index()
print(f"Indexed {stats.total_chunks} chunks from {stats.total_files} files")

# Search
results = engine.search("meetings about project alpha", top_k=5)
for r in results.results:
    print(f"{r.source_path}: {r.score:.3f}")
    print(f"  {r.content[:100]}...")

# Search with reasoning (if enabled)
results = engine.search_with_reasoning(
    "what decisions were made about authentication?",
    top_k=5,
    min_confidence=0.7,
)
for c in results.conclusions:
    print(f"[{c.type}] {c.statement}")
    print(f"  Source: {c.source_path}")
```

### CLI

```bash
# Index vault
uv run obsidian-rag index --vault /path/to/vault

# Search
uv run obsidian-rag search "project alpha status" --vault /path/to/vault

# Get stats
uv run obsidian-rag stats --vault /path/to/vault
```

### MCP Server

Start the server and connect via MCP protocol:

```bash
uv run obsidian-rag serve --vault /path/to/vault
```

The server exposes tools via JSON-RPC over stdio, compatible with any MCP client.

## Incremental Indexing

The indexer tracks file hashes. Re-running `index()` only processes changed files:

```python
# First run: indexes all files
engine.index()  # Indexed 500 files

# After adding 10 new files
engine.index()  # Indexed 10 files (skipped 500 unchanged)
```

This makes it efficient to run after each dump cycle.

## Scheduling

### Linux/macOS (cron)

```bash
# Run indexing every hour
0 * * * * cd /path/to/obsidian-rag-mcp && uv run obsidian-rag index --vault /path/to/vault
```

### Windows (Task Scheduler)

Create a batch file `index-vault.bat`:

```batch
@echo off
cd C:\path\to\obsidian-rag-mcp
uv run obsidian-rag index --vault C:\path\to\vault
```

Schedule it via Task Scheduler.

## Integration Patterns

### Pattern 1: Shared Vault Directory

Your agent writes to the same directory the MCP server reads:

```
Agent → writes → /vault/daily/2024-02-14.md
MCP Server → indexes → /vault/
Claude → queries → "what did I do yesterday?"
```

### Pattern 2: Sync + Index Pipeline

```bash
#!/bin/bash
# Daily pipeline
./your-agent-dump.sh        # Dumps to /vault/
uv run obsidian-rag index --vault /vault/  # Re-index
```

### Pattern 3: Watch Mode (Future)

A file watcher can trigger re-indexing on changes. Not yet implemented, but the incremental indexer makes this efficient.

## Tips

1. **Use consistent filenames**: `YYYY-MM-DD-topic.md` helps with date-based queries
2. **Tag liberally**: Tags enable filtered search (`search_by_tag`)
3. **Keep chunks small**: Long documents should use `## sections`
4. **Index frequently**: Incremental indexing is fast (~seconds for small changes)
5. **Enable reasoning for decisions**: The reasoning layer extracts conclusions, useful for "what was decided about X?" queries

## Performance

| Vault Size | Index Time | Query Time | Memory |
|------------|------------|------------|--------|
| 100 files | ~30s | <200ms | ~200MB |
| 500 files | ~2min | <300ms | ~300MB |
| 1000 files | ~4min | <400ms | ~400MB |

Reasoning layer adds ~1-2s per batch of 5 chunks during indexing.
