# Project Log: Obsidian RAG MCP Server

## Project Goal
Build a RAG system that allows Claude Code to semantically search an Obsidian vault containing DevOps RCA reports and documentation.

---

## Session 1: 2026-01-29

### Phase 1: Planning & Architecture (18:05-18:10)
- Created project structure
- Wrote ARCHITECTURE.md with system design
- Chose technology stack:
  - Python (Daniel's preference)
  - ChromaDB (local vector DB, no external services)
  - OpenAI embeddings (already have API key)
  - MCP protocol (for Claude Code integration)

### Phase 2: Core Implementation (18:10-18:15)
- Implemented markdown-aware chunker (respects headers, code blocks, frontmatter)
- Created OpenAI embedder wrapper with batching
- Built vault indexer with incremental update support
- Developed RAG query engine

### Phase 3: Dependency Issues (18:15-18:17)
**Problem:** Python 3.14 (system default) is too new for many packages
- ChromaDB depends on onnxruntime which has no Python 3.14 wheels
- Spent time debugging dependency resolution failures

**Solution:** Installed Python 3.12 via Homebrew
```bash
brew install python@3.12
python3.12 -m venv .venv
```

**Lesson:** Check Python version compatibility early. Bleeding-edge Python versions often lack package support.

### Phase 4: Testing & Validation (18:17-18:20)
- Generated 100+ sample RCA documents with realistic content
- Successfully indexed 132 files → 1154 chunks
- Tested semantic search - works well!
- Fixed ChromaDB API change ($contains no longer supported in where clause)

### Current Status
- ✅ Core RAG system working
- ✅ MCP tools defined
- ⏳ MCP server end-to-end test pending
- ⏳ GitHub push pending

### Key Learnings So Far
1. **Dependency hell is real** - Python 3.14 broke everything
2. **ChromaDB API changes** - Had to adapt filtering approach
3. **Chunking matters** - Markdown-aware chunking preserves document structure
4. **Embeddings are cheap** - ~$0.02 for 132 docs with OpenAI

---

## Notes for Report
- Document the Python version issue prominently
- Include cost analysis
- Show search quality examples
- Discuss MCP integration approach
