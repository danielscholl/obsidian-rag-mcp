---
status: proposed
date: 2026-01-31
---

# Memory as Reasoning: Future Architecture Direction

## Context

Traditional RAG systems treat memory as static storage: chunk documents, embed them, retrieve by similarity. This works but has limitations:

- Static artifacts don't capture implications, relationships, or patterns
- Retrieval depends on query-time similarity matching what was baked in at storage
- No mechanism for self-improvement or learning from prediction errors
- Contradictions and updates are handled poorly

Research from Plastic Labs ("Memory as Reasoning") and OpenAI's internal data agent suggest a more powerful paradigm: treating memory as a dynamic reasoning task rather than storage.

## The Insight

Human cognition doesn't just store facts - it builds *models* through prediction and surprisal:

1. Make predictions about the world/people
2. Check predictions against new information
3. Update the model based on surprisal (prediction errors)
4. Produce better predictions next time

LLMs can do this better than humans because they:
- Don't have energy/attention constraints
- Can reason from first principles cheaply
- Update without cognitive bias or belief resistance
- Have "perfect" memory of their context

## Current Architecture (Phase 1)

```
Document → Chunk → Embed → Store in ChromaDB → Retrieve by similarity
```

This is the standard RAG pattern. It works for basic semantic search.

## Proposed Future Architecture (Phase 2+)

### Layer 1: Raw Storage (current)
- Chunked documents with embeddings
- Metadata (tags, frontmatter, paths)
- Basic similarity retrieval

### Layer 2: Reasoned Conclusions
At index time, extract logical conclusions from documents:

- **Deductive**: Certain conclusions from explicit statements
  - "Document states X explicitly"
- **Inductive**: Patterns from observations
  - "Documents about service Y frequently mention timeout issues"
- **Abductive**: Best explanations for behaviors
  - "The likely root cause pattern across these RCAs is connection pool exhaustion"

Store conclusions with:
- The conclusion itself
- Supporting premises (with references to source documents)
- Certainty qualification (in natural language, not arbitrary scores)
- Timestamp and version

### Layer 3: Compositional Retrieval
At query time:
1. Find relevant raw chunks (current approach)
2. Find relevant reasoned conclusions
3. Compose conclusions dynamically to answer the query
4. Show reasoning trace with source attribution

### Layer 4: Self-Improving Memory
When the system makes predictions that are corrected:
1. Capture the correction as surprisal
2. Update or create new conclusions
3. Re-weight related conclusions
4. Build a learning loop

## Design Implications

To support this architecture, we should design Phase 1 with these hooks:

1. **Extensible storage schema** - Room for conclusion storage alongside chunks
2. **Document provenance** - Every piece of context traces back to source
3. **Metadata flexibility** - Support for reasoning metadata (premises, certainty, timestamps)
4. **Retrieval abstraction** - Engine interface that can be extended beyond similarity search

## Trade-offs

**Benefits:**
- Richer context that captures implications, not just content
- Self-improving system that learns from corrections
- Composable answers that synthesize across documents
- Better handling of contradictions and updates

**Costs:**
- More LLM calls at index time (cost + latency)
- More complex storage and retrieval logic
- Reasoning quality depends on model capability
- Need evaluation framework to measure reasoning quality

## Implementation Phases

1. **Phase 1 (current)**: Basic RAG - chunks, embeddings, similarity search
2. **Phase 2**: Add conclusion extraction at index time
3. **Phase 3**: Compositional retrieval with reasoning traces
4. **Phase 4**: Self-improving memory with surprisal-based updates

## References

- Plastic Labs: "Memory as Reasoning" - https://blog.plasticlabs.ai/blog/Memory-as-Reasoning
- OpenAI: "Inside OpenAI's in-house data agent" (internal context layers, especially Layer 5-6)
- Chain-of-thought prompting: https://arxiv.org/abs/2205.11916
- DeepSeek R1 reasoning models: https://github.com/deepseek-ai/DeepSeek-R1

## Decision

Adopt memory-as-reasoning as the long-term architectural direction. Design Phase 1 with extensibility hooks. Implement reasoning layers in Phase 2+.

This ADR captures the vision; specific implementation decisions will be documented in subsequent ADRs as we build each phase.
