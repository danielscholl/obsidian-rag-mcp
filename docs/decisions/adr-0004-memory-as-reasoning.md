# ADR-0004: Memory as Reasoning

**Status:** Accepted  
**Date:** 2026-01-31  
**Context:** Future architecture direction for obsidian-rag-mcp

## Context

Traditional RAG systems treat memory as static storage:
- Chunk documents → embed → store in vector DB → retrieve by similarity

This approach has limitations:
- Assumes you know what's worth storing upfront
- Stored artifacts are static once indexed
- Success depends on search strategy aligning with storage structure
- No learning or improvement over time

Research from [Plastic Labs](https://blog.plasticlabs.ai/blog/Memory-as-Reasoning) proposes a fundamentally different approach: **memory as a reasoning task**.

## Decision

We will architect obsidian-rag-mcp with extensibility hooks to support memory-as-reasoning in future phases, while delivering basic RAG functionality first.

### Core Insight

Human cognition uses prediction and surprisal, not perfect recall:
- Make predictions based on incomplete data
- Check for errors (surprisal) at the margins
- Update internal model to improve future predictions

LLMs can do this *better* than humans because they:
- Reason from first principles cheaply
- Generate inferences nearly effortlessly
- Have no cognitive bias or belief resistance
- Can be trained on hard reasoning tasks

### Reasoning Types to Capture

1. **Deductive**: Certain conclusions from explicit premises
2. **Inductive**: General statements from observed patterns  
3. **Abductive**: Best explanation for observed behaviors

### Phased Implementation

#### Phase 1: Basic RAG (Current)
- Markdown-aware chunking ✅
- OpenAI embeddings ✅
- ChromaDB vector storage ✅
- Semantic search via MCP ✅

**Design hooks for future:**
- Chunk metadata is extensible (can add `conclusions`, `certainty`)
- Indexer pipeline is modular (can insert reasoning step)
- Engine supports filtering (can filter by conclusion type)

#### Phase 2: Reasoning Layer
- At index time, extract conclusions from each chunk
- Store conclusions with:
  - Premises (source chunks)
  - Reasoning type (deductive/inductive/abductive)
  - Certainty level (high/medium/low)
- Compositional retrieval: find conclusions, trace to sources

#### Phase 3: Self-Improving Memory
- Capture surprisal (when predictions are wrong)
- Update conclusions based on corrections
- Build feedback loop for continuous improvement
- Track conclusion accuracy over time

## Consequences

### Positive
- Clear north star for project evolution
- Phase 1 delivers value immediately
- Architecture won't need major refactoring for Phase 2
- Aligns with cutting-edge research direction

### Negative
- Phase 2+ requires significant additional work
- Reasoning extraction adds latency to indexing
- More complex mental model for contributors

### Risks
- Reasoning quality depends on LLM capability
- May need fine-tuning for domain-specific reasoning
- Cost increases with reasoning step (more API calls)

## References

- [Memory as Reasoning - Plastic Labs](https://blog.plasticlabs.ai/blog/Memory-as-Reasoning)
- [Chain-of-Thought Prompting](https://arxiv.org/abs/2205.11916)
- [OpenAI o1 Technical Report](https://arxiv.org/abs/2412.16720)
- [DeepSeek R1](https://github.com/deepseek-ai/DeepSeek-R1)
- [Honcho](https://honcho.dev) - Plastic Labs' implementation
