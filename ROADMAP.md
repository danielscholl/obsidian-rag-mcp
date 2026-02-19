# Roadmap

> Semantic search for Obsidian → Reasoning layer → Self-improving memory

## Overview

This project evolves through three phases, each building on the last. Phase 1 is complete. We're currently hardening before moving to Phase 2.

```
[Phase 1: Core RAG] ✅ → [Hardening] → [Phase 2: Reasoning] → [Phase 3: Self-Improving]
     Done              ← You are here
```

---

## ✅ Phase 1: Core RAG (Complete)

**Goal:** Basic semantic search that works.

**Delivered:**
- Markdown-aware chunking (respects headers, code blocks, frontmatter)
- OpenAI embeddings with batching and retries
- ChromaDB vector storage (local, no external services)
- MCP server with 5 tools for Claude Code integration
- CLI for indexing and search
- 40+ tests, CI/CD, security hardening

**Try it:**
```bash
obsidian-rag index ./vault
obsidian-rag search "database connection issues"
```

---

## 🔧 Hardening & Polish (Current)

**Goal:** Production-ready quality before adding features.

**Target:** End of February 2026

| Issue | Description |
|-------|-------------|
| [#21](../../issues/21) | Fix empty query crash |
| [#22](../../issues/22) | CLI input validation |
| [#13](../../issues/13) | Fix .venv ignore pattern |
| [#7](../../issues/7) | Claude Code integration test |
| [#8](../../issues/8) | Local development docs |
| [#17](../../issues/17) | README/Architecture refresh |
| [#23](../../issues/23) | PyPI publishing |

**Track progress:** [Milestone](../../milestone/4)

---

## 🧠 Phase 2: Reasoning Layer (Next)

**Goal:** Don't just find similar text—extract and compose conclusions.

**Target:** End of March 2026

**The idea:** Instead of returning raw chunks, extract logical conclusions at index time and compose answers with reasoning traces.

```
Current:  Query → Find similar chunks → Return text
Phase 2:  Query → Find conclusions → Compose answer with reasoning
```

| Issue | Description |
|-------|-------------|
| [#14](../../issues/14) | Reasoning layer at index time |
| [#15](../../issues/15) | Compositional retrieval with traces |
| [#18](../../issues/18) | Incremental indexing |

**Key features:**
- **Deductive conclusions:** "Document states X explicitly"
- **Inductive conclusions:** "Pattern Y appears across these RCAs"
- **Abductive conclusions:** "Most likely explanation is Z"
- **Reasoning traces:** Show HOW the answer was composed

**Track progress:** [Milestone](../../milestone/2)

**Reference:** [ADR-0004](docs/decisions/adr-0004-memory-as-reasoning.md)

---

## 🔄 Phase 3: Self-Improving Memory (Future)

**Goal:** Learn from corrections and improve over time.

**Target:** Mid 2026

**The idea:** When predictions are wrong (surprisal), update the model.

```
User asks → System answers → User corrects → System learns → Better next time
```

| Issue | Description |
|-------|-------------|
| [#16](../../issues/16) | Self-improving memory via surprisal |

**Key features:**
- Capture corrections (explicit feedback or implicit signals)
- Update conclusions based on corrections
- Track prediction accuracy over time
- Build learning loop

**Track progress:** [Milestone](../../milestone/3)

---

## Research Foundation

This roadmap is informed by:

- [Memory as Reasoning](https://blog.plasticlabs.ai/blog/Memory-as-Reasoning) - Plastic Labs
- [Chain-of-Thought Prompting](https://arxiv.org/abs/2205.11916)
- [OpenAI o1 Technical Report](https://arxiv.org/abs/2412.16720)

The core insight: memory isn't static storage—it's a reasoning task. LLMs can build logical conclusion trees that exceed human performance because they lack cognitive biases and resource constraints.

---

## Contributing

Want to help? Check the [current milestone](../../milestones) for open issues. All contributions go through PRs (branch protection enabled).

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup.
