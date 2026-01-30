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

### Phase 5: MCP Protocol Integration (18:20-18:25)
**Problem:** MCP SDK's `stdio_server` is an async context manager, not a coroutine
- Initial code: `asyncio.run(stdio_server(server))` ❌
- Fixed code: `async with stdio_server() as streams:` ✅

**Lesson:** Read SDK source code when docs are unclear. The MCP Python SDK is well-written but documentation is sparse.

### Phase 6: GitHub Push (18:25)
- Created public repo: https://github.com/claudiogarza/obsidian-rag-mcp
- Pushed all code with clean commit history

---

## Final Project Stats

| Metric | Value |
|--------|-------|
| Time to working prototype | ~25 minutes |
| Lines of Python code | ~800 |
| Sample RCA documents | 111 |
| Total indexed chunks | 1,154 |
| Embedding cost | ~$0.02 |
| Dependencies | 50+ (ChromaDB brings many) |

---

## Challenges Encountered

1. **Python 3.14 Compatibility**
   - onnxruntime has no wheels for 3.14
   - Solution: Use Python 3.12

2. **ChromaDB API Changes**
   - `$contains` filter removed in newer versions
   - Solution: Use `where_document` for content filtering

3. **MCP SDK Usage**
   - Sparse documentation
   - Solution: Read source code, trial and error

---

## What Went Well

1. **OpenAI Embeddings** - Just worked, cheap, good quality
2. **ChromaDB** - Local, fast, no external services
3. **Markdown Chunking** - Preserving document structure improved search quality
4. **Sample Data Generation** - Realistic RCAs made testing meaningful

---

## Session 2: 2026-01-29 (Continued)

### Phase 7: Code Review & Production Hardening (18:30-18:45)

Conducted comprehensive code review and implemented production improvements:

#### Tests Added (34 total)
- `test_chunker.py` - 13 tests covering H2 splitting, code block preservation, tag extraction
- `test_embedder.py` - 8 tests covering batching, retry logic, text cleaning
- `test_engine.py` - 13 tests covering search, filtering, security

#### Security Improvements
- **Fixed path traversal timing issue** - Now checks path containment BEFORE existence (prevents information disclosure)
- Added input validation for all MCP tools (bounds checking, sanitization)
- Added query length limits (8k chars for queries, 30k for documents)

#### Reliability Improvements
- **Added retry logic** with exponential backoff for OpenAI API calls (tenacity)
- Added proper logging throughout (replaced print() statements)
- Added vault path validation on indexer initialization
- Better error handling with specific exception types

#### Code Quality
- Fixed mutable default argument annotation (`Optional[list[str]]` instead of `list[str] = None`)
- Added bounds checking for `top_k` (1-50) and `limit` (1-100) parameters
- Added logging configuration for MCP server

### Code Review Summary (by sub-agent)

| Area | Grade | Notes |
|------|-------|-------|
| Code Quality | **B+** | Clean, but had some anti-patterns |
| Architecture | **B+** | Sound choices, some coupling issues |
| Error Handling | **C+** → **B+** | Improved with retries and validation |
| Security | **B** → **A-** | Path traversal fixed |
| Documentation | **A-** | Architecture doc is excellent |

**Overall:** Solid MVP, now production-hardened.

---

## Notes for Report
- Document the Python version issue prominently
- Include cost analysis
- Show search quality examples
- Discuss MCP integration approach
- Highlight test coverage and security improvements
