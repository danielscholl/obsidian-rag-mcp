# Architecture: Obsidian RAG MCP Server

## Overview

This system provides semantic search capabilities over an Obsidian vault, exposed as an MCP (Model Context Protocol) server for integration with Claude Code and other MCP-compatible AI tools.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Claude Code                               │
│                            │                                     │
│                      MCP Protocol                                │
│                            │                                     │
│                            ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Obsidian RAG MCP Server                     │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │   │
│  │  │ MCP Layer   │  │ RAG Engine  │  │ Vault Indexer   │  │   │
│  │  │ (Tools)     │◄─│ (Query)     │◄─│ (Watch/Index)   │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────────┘  │   │
│  │         │                │                  │            │   │
│  │         │                ▼                  │            │   │
│  │         │        ┌─────────────┐           │            │   │
│  │         │        │  ChromaDB   │◄──────────┘            │   │
│  │         │        │ (Vectors)   │                        │   │
│  │         │        └─────────────┘                        │   │
│  └─────────│────────────────────────────────────────────────┘   │
│            │                                                     │
│            ▼                                                     │
│  ┌─────────────────────┐    ┌─────────────────────────────┐    │
│  │  OpenAI Embeddings  │    │     Obsidian Vault          │    │
│  │  (text-embedding-   │    │     (Markdown Files)        │    │
│  │   3-small)          │    │                             │    │
│  └─────────────────────┘    └─────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### 1. Vault Indexer (`src/rag/indexer.py`)

**Responsibility:** Scan, chunk, and embed Obsidian vault content.

**Key Features:**
- Markdown-aware chunking (respects headers, code blocks, frontmatter)
- Incremental indexing (only re-index changed files)
- Metadata extraction (tags, frontmatter, links)
- File watching for auto-reindex

**Chunking Strategy:**
- Split on H2 headers (`##`) as primary boundaries
- Maximum chunk size: 1000 tokens
- Overlap: 100 tokens between chunks
- Preserve code blocks and tables as atomic units

### 2. RAG Engine (`src/rag/engine.py`)

**Responsibility:** Query the vector database and retrieve relevant context.

**Key Features:**
- Semantic search with configurable top-k
- Hybrid search (semantic + keyword for tags/metadata)
- Re-ranking for improved relevance
- Context assembly with source attribution

**Query Pipeline:**
1. Embed query using OpenAI
2. Vector similarity search in ChromaDB
3. Optional: Filter by metadata (tags, date range, path)
4. Return ranked results with snippets and source paths

### 3. MCP Server (`src/mcp/server.py`)

**Responsibility:** Expose RAG capabilities via MCP protocol.

**Tools Provided:**

| Tool | Description |
|------|-------------|
| `search_vault` | Semantic search across all vault content |
| `search_by_tag` | Search filtered by Obsidian tags |
| `get_related` | Find notes related to a given note |
| `get_note` | Retrieve full content of a specific note |
| `list_recent` | List recently modified notes |
| `index_status` | Check indexing status and stats |

**Resources Provided:**
- `vault://stats` - Vault statistics (note count, index size, etc.)

### 4. CLI (`src/cli/main.py`)

**Responsibility:** Command-line interface for testing and management.

**Commands:**
- `index` - Index/reindex the vault
- `search <query>` - Test semantic search
- `serve` - Start MCP server
- `stats` - Show index statistics

## Data Flow

### Indexing Flow

```
Obsidian Vault
      │
      ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│ File Reader │───▶│ MD Chunker   │───▶│ Embedder    │
│             │    │ + Metadata   │    │ (OpenAI)    │
└─────────────┘    └──────────────┘    └─────────────┘
                                              │
                                              ▼
                                       ┌─────────────┐
                                       │  ChromaDB   │
                                       │  (persist)  │
                                       └─────────────┘
```

### Query Flow

```
User Query (via MCP)
      │
      ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│ Query       │───▶│ Embedder     │───▶│ ChromaDB    │
│ Parser      │    │ (OpenAI)     │    │ (search)    │
└─────────────┘    └──────────────┘    └─────────────┘
                                              │
                                              ▼
                                       ┌─────────────┐
                                       │ Ranker &    │
                                       │ Formatter   │
                                       └─────────────┘
                                              │
                                              ▼
                                       Search Results
```

## Technology Choices

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Language | Python 3.11+ | Rich ML ecosystem, MCP SDK support |
| Vector DB | ChromaDB | Local, no external deps, good for <10k docs |
| Embeddings | OpenAI text-embedding-3-small | Cost-effective, high quality |
| MCP SDK | mcp (official Python SDK) | Official Anthropic SDK |
| Markdown | mistune | Fast, extensible MD parser |

## Security Considerations

1. **API Keys**: Stored in environment variables, never committed
2. **Local-first**: ChromaDB runs locally, no data leaves machine (except embeddings)
3. **Input Validation**: All file paths validated against vault root
4. **No Code Execution**: RAG is read-only, no eval/exec of vault content
5. **Trusted Dependencies**: Only well-known packages from PyPI

## File Structure

```
obsidian-rag-mcp/
├── src/
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── indexer.py      # Vault scanning and indexing
│   │   ├── chunker.py      # Markdown-aware chunking
│   │   ├── embedder.py     # OpenAI embedding wrapper
│   │   └── engine.py       # Query and retrieval
│   ├── mcp/
│   │   ├── __init__.py
│   │   └── server.py       # MCP server implementation
│   └── cli/
│       ├── __init__.py
│       └── main.py         # CLI entry point
├── tests/
│   ├── test_indexer.py
│   ├── test_chunker.py
│   └── test_engine.py
├── vault/                   # Sample vault for testing
│   ├── RCAs/
│   ├── Runbooks/
│   └── Services/
├── docs/
│   ├── ARCHITECTURE.md     # This file
│   └── SETUP.md            # Installation guide
├── scripts/
│   └── seed_vault.py       # Generate sample RCA documents
├── pyproject.toml          # Project config
├── README.md
└── .env.example
```

## Performance Targets

| Metric | Target |
|--------|--------|
| Index 100 notes | < 60 seconds |
| Query latency | < 500ms |
| Memory usage | < 500MB |
| Embedding cost | ~$0.02 per full reindex |

## Future Enhancements

1. **Local Embeddings**: Option to use sentence-transformers for offline/free operation
2. **Incremental Sync**: Watch mode for real-time index updates
3. **Graph Awareness**: Leverage Obsidian links for context expansion
4. **Caching**: Query result caching for repeated questions
5. **Multi-vault**: Support multiple vault sources
