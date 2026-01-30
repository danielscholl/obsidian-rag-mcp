---
status: accepted
date: 2026-01-29
---

# Use OpenAI Embeddings for Semantic Search

## Context

Semantic search requires converting text into vector embeddings. We need to choose an embedding model that balances quality, cost, and operational simplicity.

## Decision Drivers

- **Quality**: Embeddings must capture semantic meaning well for RAG use cases
- **Cost**: Indexing hundreds of documents should cost pennies, not dollars
- **Simplicity**: Prefer API over self-hosted models for MVP
- **Latency**: Query embedding should be fast (<100ms)

## Considered Options

1. **OpenAI text-embedding-3-small** — API, $0.02/1M tokens
2. **OpenAI text-embedding-3-large** — API, $0.13/1M tokens, higher quality
3. **Sentence Transformers (local)** — Free, self-hosted, CPU/GPU
4. **Cohere Embed** — API, competitive pricing
5. **Voyage AI** — API, optimized for RAG

## Decision

**OpenAI text-embedding-3-small** — Best balance of quality, cost, and simplicity for our use case.

## Consequences

**Good:**
- Excellent quality for the price point
- Simple API, no infrastructure to manage
- Fast (sub-100ms for typical queries)
- Cost is negligible (~$0.02 per 100 documents)

**Bad:**
- Requires API key and internet connection
- Data leaves the local machine (embedding vectors, not raw content)
- Vendor dependency

**Mitigations:**
- Future: Add Sentence Transformers option for fully offline use
- Embedder interface is abstracted, allowing backend swaps

## Cost Analysis

Typical vault (100 documents, ~2000 tokens each):
- Full reindex: ~200k tokens = ~$0.004
- Per query: ~100 tokens = ~$0.000002

At this cost level, there's no practical reason to optimize further for MVP.

## Notes

Consider adding local embedding option (Sentence Transformers) for users who need fully offline operation or have compliance requirements.
