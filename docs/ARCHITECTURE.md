# Architecture: Obsidian RAG MCP Server

## Overview

Semantic search over markdown vaults, exposed as an MCP server for AI assistants.

```
┌─────────────────────────────────────────────────────────────────┐
│                     Claude Desktop / MCP Client                  │
│                              │                                   │
│                        MCP Protocol                              │
│                              ▼                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                 Obsidian RAG MCP Server                    │  │
│  │                                                            │  │
│  │   ┌──────────┐   ┌──────────┐   ┌──────────────────────┐  │  │
│  │   │   MCP    │   │   RAG    │   │    Vault Indexer     │  │  │
│  │   │  Tools   │◄──│  Engine  │◄──│  (scan/chunk/embed)  │  │  │
│  │   └──────────┘   └────┬─────┘   └──────────────────────┘  │  │
│  │                       │                    │               │  │
│  │                       ▼                    ▼               │  │
│  │              ┌─────────────────────────────────┐          │  │
│  │              │          ChromaDB               │          │  │
│  │              │   ┌─────────┐  ┌────────────┐   │          │  │
│  │              │   │ Chunks  │  │ Conclusions│   │          │  │
│  │              │   │(vectors)│  │ (Phase 2)  │   │          │  │
│  │              │   └─────────┘  └────────────┘   │          │  │
│  │              └─────────────────────────────────┘          │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                   │
│              ┌───────────────┴───────────────┐                  │
│              ▼                               ▼                  │
│    ┌──────────────────┐           ┌──────────────────┐         │
│    │ OpenAI Embeddings│           │  Markdown Vault  │         │
│    │ (text-embedding- │           │   (.md files)    │         │
│    │  3-small)        │           │                  │         │
│    └──────────────────┘           └──────────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### 1. Vault Indexer (`obsidian_rag_mcp/rag/indexer.py`)

Scans, chunks, and embeds vault content.

- **Markdown-aware chunking**: Respects headers, code blocks, frontmatter
- **Incremental indexing**: Only re-indexes changed files (by content hash)
- **Metadata extraction**: Tags, frontmatter, links
- **Reasoning extraction**: Optional LLM-based conclusion extraction

### 2. RAG Engine (`obsidian_rag_mcp/rag/engine.py`)

Query interface for semantic search.

- **Semantic search**: Vector similarity via ChromaDB
- **Tag filtering**: Filter by Obsidian tags
- **Reasoning search**: Search over extracted conclusions
- **Source attribution**: All results link to source files

### 3. Reasoning Layer (`obsidian_rag_mcp/reasoning/`)

*Phase 2 feature* - Extracts logical conclusions from content.

```
obsidian_rag_mcp/reasoning/
├── extractor.py       # LLM-based conclusion extraction
├── conclusion_store.py # ChromaDB storage for conclusions
└── models.py          # Conclusion, ConclusionType dataclasses
```

**Conclusion types:**
- `deductive`: Logically follows from premises
- `inductive`: Pattern-based generalization
- `abductive`: Best explanation inference

**Features:**
- Batch extraction (reduces API calls)
- Extraction caching (skip unchanged chunks)
- Confidence scoring
- Source linking (conclusion → source chunk)

### 4. MCP Server (`obsidian_rag_mcp/mcp/server.py`)

Exposes RAG capabilities via MCP protocol.

**Tools:**

| Tool | Description |
|------|-------------|
| `search_vault` | Semantic search across all content |
| `search_by_tag` | Filter by Obsidian tags |
| `get_note` | Retrieve full note content |
| `get_related` | Find similar notes |
| `list_recent` | Recently modified notes |
| `index_status` | Index statistics |
| `search_with_reasoning` | Search with conclusions |
| `get_conclusion_trace` | Trace reasoning chain |
| `explore_connected_conclusions` | Find related conclusions |

### 5. CLI (`obsidian_rag_mcp/cli/main.py`)

Command-line interface.

```bash
obsidian-rag index --vault /path     # Index vault
obsidian-rag search "query"          # Search
obsidian-rag serve --vault /path     # Start MCP server
obsidian-rag stats --vault /path     # Show statistics
```

## Data Flow

### Indexing

```
Vault Files → Chunker → Embedder → ChromaDB
                │
                └──→ Extractor → Conclusions (if reasoning enabled)
```

### Query

```
Query → Embed → ChromaDB Search → Rank → Results
                     │
                     └──→ Conclusion Search (if reasoning enabled)
```

## Technology Stack

| Component | Choice | Why |
|-----------|--------|-----|
| Language | Python 3.11+ | MCP SDK, ML ecosystem |
| Vector DB | ChromaDB | Local, embedded, simple |
| Embeddings | OpenAI text-embedding-3-small | Quality + cost balance |
| MCP | Official Python SDK | Anthropic standard |
| Async | asyncio | Non-blocking MCP server |

## File Structure

```
obsidian-rag-mcp/
├── obsidian_rag_mcp/
│   ├── rag/              # Core RAG
│   │   ├── indexer.py    # Vault indexing
│   │   ├── chunker.py    # Markdown chunking
│   │   ├── embedder.py   # OpenAI embeddings
│   │   └── engine.py     # Search engine
│   ├── reasoning/        # Phase 2: Conclusions
│   │   ├── extractor.py
│   │   ├── conclusion_store.py
│   │   └── models.py
│   ├── mcp/
│   │   └── server.py     # MCP server
│   └── cli/
│       └── main.py       # CLI
├── tests/                # pytest tests
├── vault/                # Sample vault
├── docs/                 # Documentation
│   ├── ARCHITECTURE.md   # This file
│   ├── DEVELOPMENT.md    # Local setup
│   ├── GETTING_STARTED.md # Quickstart + Claude Desktop setup
│   ├── INTEGRATION.md    # Integration guide
│   └── decisions/        # ADRs
└── pyproject.toml
```

## Security

- **Local-first**: ChromaDB runs locally, vectors never leave machine
- **API keys**: Environment variables only, never committed
- **Path validation**: All file access validated against vault root
- **Read-only**: No code execution, no file writes to vault

## Performance

| Metric | Target | Actual |
|--------|--------|--------|
| Index 100 notes | <60s | ~30s |
| Query latency | <500ms | ~200ms |
| Memory | <500MB | ~300MB |

## Architecture Decision Records

See `docs/decisions/` for rationale:
- [ADR-0001](decisions/adr-0001-chromadb.md): ChromaDB as vector store
- [ADR-0002](decisions/adr-0002-ci-health-checks.md): CI pipeline
- [ADR-0003](decisions/adr-0003-openai-embeddings.md): OpenAI embeddings
- [ADR-0004](decisions/adr-0004-memory-as-reasoning.md): Reasoning layer design
