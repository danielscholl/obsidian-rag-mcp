# Self-Improving RAG Systems for Personal Knowledge Bases
## Independent Research Perspective

**Date:** 2025-01-27  
**Context:** Obsidian vault RAG system with feedback-driven improvement  
**Scope:** Local-first, privacy-preserving, practical implementation

---

## Executive Summary

Self-improving RAG is fundamentally a **learning-to-rank** problem with unique constraints: sparse feedback, single-user personalization, cold start challenges, and privacy requirements. The most effective approaches combine **lightweight online learning** with **implicit behavioral signals**, avoiding the complexity of full model retraining.

Key insight: Personal knowledge RAG benefits enormously from **temporal and contextual priors** that general RAG systems ignore. Your notes have structure, recency patterns, and semantic neighborhoods that encode implicit relevance.

---

## 1. Most Valuable Feedback Signals

### Tier 1: High-Signal, Low-Friction (Prioritize These)

| Signal | Implementation | Value |
|--------|----------------|-------|
| **Click-through / Selection** | Track which retrieved chunks user expands, copies, or follows links to | Direct relevance indicator |
| **Dwell time** | Time spent viewing a retrieved result before returning to query | Engagement proxy |
| **Copy/paste behavior** | User copies text from a specific chunk | Strong positive signal |
| **Follow-up queries** | Query refinement patterns (narrowing = good retrieval, broadening = poor) | Session-level feedback |
| **Answer acceptance** | User proceeds vs. rephrases the question | Implicit satisfaction |

### Tier 2: Structural Signals (Free, Often Overlooked)

| Signal | Implementation | Value |
|--------|----------------|-------|
| **Note edit proximity** | User edits a note shortly after retrieval | Very strong relevance |
| **Link creation** | User creates a link to/from retrieved note | Semantic relationship confirmed |
| **Note co-access patterns** | Notes frequently accessed in same session | Latent topic clustering |
| **Temporal decay** | Recent notes often more relevant | Freshness prior |
| **Backlink density** | Highly-linked notes are often authoritative | PageRank-style signal |

### Tier 3: Explicit Feedback (Use Sparingly)

| Signal | Implementation | Value |
|--------|----------------|-------|
| **Thumbs up/down** | Binary rating on retrieval quality | Clean but adds friction |
| **"Not helpful" button** | Negative signal on specific chunks | Valuable for learning what to demote |
| **Star/save result** | User marks a result as valuable | Strong positive, rare event |

### Recommendation: **Implicit-First Strategy**
Explicit feedback suffers from:
- Selection bias (users rate extremes, not middle)
- Feedback fatigue (ratings drop over time)
- Single-user sparsity (you won't generate enough explicit signals)

**80% of learning should come from implicit signals.** Reserve explicit feedback for calibration and edge cases.

---

## 2. Learning Algorithms: Simplicity vs. Effectiveness

### Algorithm Comparison Matrix

| Algorithm | Complexity | Cold Start | Convergence | Local-First Fit | Recommendation |
|-----------|------------|------------|-------------|-----------------|----------------|
| **Online Gradient Descent** | Low | Handles well | Fast | Excellent | ⭐ Primary choice |
| **Thompson Sampling** | Low | Excellent | Moderate | Excellent | ⭐ For exploration |
| **LambdaMART** | High | Poor | Slow | Moderate | For batch retraining |
| **Neural re-ranker fine-tuning** | Very High | Poor | Slow | Poor | Avoid for personal |
| **Multi-armed bandit** | Very Low | Good | Fast | Excellent | For A/B chunk selection |
| **Bayesian Personalized Ranking** | Moderate | Moderate | Moderate | Good | For pairwise preferences |

### Recommended: Two-Layer Architecture

```
┌─────────────────────────────────────────────────┐
│           Layer 1: Fast Online Learning         │
│  ┌─────────────────────────────────────────┐   │
│  │  Lightweight Re-ranker                   │   │
│  │  - Linear model over retrieval features  │   │
│  │  - Online gradient descent updates       │   │
│  │  - Updates on every interaction          │   │
│  │  - ~100 parameters                       │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│         Layer 2: Periodic Refinement            │
│  ┌─────────────────────────────────────────┐   │
│  │  Embedding Space Adjustment              │   │
│  │  - Contrastive fine-tuning on feedback   │   │
│  │  - Runs weekly/monthly in background     │   │
│  │  - Adjusts retrieval, not just ranking   │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

### Layer 1: Online Linear Re-ranker (Primary)

**Features to learn weights for:**
```python
features = [
    "semantic_similarity",      # Base embedding cosine sim
    "bm25_score",               # Lexical match score
    "recency_score",            # Exponential decay from last modified
    "access_frequency",         # How often you visit this note
    "backlink_count",           # Normalized in-degree
    "query_term_coverage",      # % of query terms in chunk
    "note_length_norm",         # Longer notes often more comprehensive
    "heading_depth",            # Chunks from H1 vs H4
    "code_block_presence",      # If query seems technical
    "historical_ctr",           # Past click-through for this note
]
```

**Update rule (simplified Online Gradient Descent):**
```python
# After user selects chunk i from candidates [1..k]
for j in [1..k]:
    if j == i:  # Selected
        weights += learning_rate * features[j]
    else:       # Not selected
        weights -= learning_rate * features[j] / (k - 1)
```

**Why this works:**
- Updates in milliseconds (no GPU needed)
- Naturally handles concept drift as your notes evolve
- Interpretable (you can see which features matter)
- Regularization via weight decay prevents overfitting

### Layer 2: Contrastive Embedding Adjustment (Secondary)

Run periodically to adjust the embedding space itself:

```python
# Collect positive pairs from feedback
positive_pairs = [
    (query_embedding, selected_chunk_embedding)
    for query, selected in feedback_log
]

# Negative samples from non-selected chunks
# Use in-batch negatives for efficiency

# Fine-tune embedding model with contrastive loss
# Or simpler: learn a small projection matrix
```

**For local-first:** Instead of fine-tuning a full embedding model, learn a lightweight **projection head** (single linear layer) that adjusts embeddings post-hoc. This is:
- Fast to train
- Easy to store/version
- Reversible if it degrades

---

## 3. Cold Start Problem Solutions

### The Challenge
New notes have no feedback history. New queries have no similar past queries. How do you provide good retrieval from day one?

### Solution 1: Structural Priors (Immediate)

Leverage Obsidian's graph structure:
```python
cold_start_score = (
    0.3 * semantic_similarity +      # Embedding baseline
    0.2 * tag_overlap +               # Shared tags with query context
    0.2 * folder_relevance +          # Same folder as recently accessed
    0.15 * backlink_authority +       # Well-linked notes are often good
    0.15 * recency_boost              # Newer notes for evolving topics
)
```

### Solution 2: Content-Based Bootstrapping

For new notes, **infer relevance from similar existing notes:**
```python
def cold_start_score(new_note, query):
    # Find k most similar notes that DO have feedback
    similar_notes = find_similar(new_note.embedding, k=5)
    
    # Inherit their learned relevance to this query type
    inherited_score = mean([
        learned_relevance(note, query) 
        for note in similar_notes
    ])
    
    return inherited_score
```

### Solution 3: Exploration via Thompson Sampling

Don't just exploit known-good results. Occasionally surface uncertain candidates:

```python
def select_with_exploration(candidates, exploitation_ratio=0.8):
    if random() < exploitation_ratio:
        return argmax(candidates, key=predicted_score)
    else:
        # Thompson sampling: sample from posterior
        return sample_from_uncertainty(candidates)
```

This naturally addresses cold start by giving new content chances to prove itself.

### Solution 4: Query Clustering and Transfer

Group similar queries, share learning across the cluster:
```python
# "How do I configure neovim?" and "neovim setup guide"
# Should share relevance knowledge

query_cluster = assign_cluster(query.embedding)
cluster_priors = get_cluster_relevance_model(query_cluster)
# Apply cluster priors, then personalize with individual feedback
```

### Solution 5: Synthetic Feedback Generation

For truly new vaults, bootstrap with synthetic preferences:
```python
# Generate pseudo-queries from note content
pseudo_query = generate_question(note.content)

# The note itself is a positive example
# Random other notes are negatives
synthetic_pair = (pseudo_query, note, random_negatives)
```

This creates a warm start before any real usage.

---

## 4. Privacy-Preserving Local-First Approaches

### Core Principle: Everything Stays Local

```
┌─────────────────────────────────────────────────┐
│                 Your Machine                     │
│  ┌─────────────┐  ┌─────────────┐              │
│  │ Obsidian    │  │ Local       │              │
│  │ Vault       │──│ Embeddings  │              │
│  └─────────────┘  └─────────────┘              │
│         │                │                       │
│         ▼                ▼                       │
│  ┌─────────────────────────────────────────┐   │
│  │         Local RAG Engine                 │   │
│  │  - Local embedding model (e.g., gte-small)│  │
│  │  - Local vector store (SQLite + vectors) │   │
│  │  - Local re-ranker weights               │   │
│  │  - Local feedback log                    │   │
│  └─────────────────────────────────────────┘   │
│                      │                           │
│                      ▼                           │
│  ┌─────────────────────────────────────────┐   │
│  │   LLM (local or API with query only)    │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

### Strategy 1: Local Embedding Models

**Recommended models for local use:**
| Model | Size | Quality | Speed |
|-------|------|---------|-------|
| `gte-small` | 33M | Good | Fast |
| `all-MiniLM-L6-v2` | 22M | Good | Very Fast |
| `bge-small-en-v1.5` | 33M | Better | Fast |
| `nomic-embed-text-v1.5` | 137M | Best | Moderate |

All run on CPU. No data leaves your machine for retrieval.

### Strategy 2: Differential Privacy for Feedback Logs

If you ever sync or backup feedback logs:
```python
# Add noise to aggregated statistics
def private_feature_weight(true_weight, epsilon=1.0):
    noise = laplace(scale=1/epsilon)
    return true_weight + noise
```

### Strategy 3: Secure Aggregation (If Multi-Device)

If syncing across devices without central server:
```python
# Each device computes local gradients
local_gradient = compute_gradient(local_feedback)

# Encrypt before sync
encrypted = encrypt(local_gradient, shared_key)

# Aggregate encrypted gradients, decrypt sum
# No single gradient is ever visible
```

### Strategy 4: Query Sanitization for LLM Calls

When sending to external LLM:
```python
def sanitize_context(retrieved_chunks):
    # Option 1: Summarize locally first
    # Option 2: Replace named entities with placeholders
    # Option 3: Use local LLM for sensitive queries
    pass
```

### Strategy 5: Embedding Non-Invertibility

Modern embeddings are difficult but not impossible to invert. For sensitive notes:
- **Don't embed them** (exclude from retrieval, use keyword match only)
- **Encrypt at rest** with separate key
- **Use noise injection** on sensitive embeddings

---

## 5. Novel Approaches You Might Be Missing

### 5.1 Cognitive Scaffolding via Spaced Retrieval

Borrow from spaced repetition: notes you haven't accessed in a while but are relevant get **boosted** to resurface knowledge.

```python
def spaced_retrieval_boost(note, query):
    if is_relevant(note, query):
        days_since_access = (now - note.last_accessed).days
        # SM-2 style boost for forgotten-but-relevant
        boost = 1 + log(1 + days_since_access) * relevance_score
        return boost
    return 1.0
```

**Why it matters:** Personal knowledge bases should help you remember, not just retrieve.

### 5.2 Query Intent Classification → Retrieval Strategy

Different query types need different retrieval:

| Intent | Strategy |
|--------|----------|
| **Lookup** ("What is X?") | High precision, single best chunk |
| **Exploration** ("What do I know about X?") | High recall, diverse results |
| **Synthesis** ("How does X relate to Y?") | Multi-hop retrieval, graph traversal |
| **Recent** ("What was I working on?") | Temporal weighting dominates |

**Classify intent, then adjust retrieval:**
```python
intent = classify_intent(query)  # Simple classifier
if intent == "lookup":
    retrieval_config = {"k": 3, "diversity": 0.1, "recency_weight": 0.1}
elif intent == "exploration":
    retrieval_config = {"k": 10, "diversity": 0.5, "recency_weight": 0.2}
# ...
```

### 5.3 Retrieval-Aware Query Rewriting

Before retrieval, expand/rewrite the query using your knowledge graph:

```python
def expand_query(query):
    # Extract entities
    entities = extract_entities(query)
    
    # Find related notes via links
    related = [note for e in entities for note in e.linked_notes]
    
    # Extract co-occurring terms
    expansion_terms = extract_key_terms(related)
    
    return query + " " + " ".join(expansion_terms)
```

### 5.4 Contrastive Chunk Boundaries

Most chunking is arbitrary (N tokens). Learn optimal chunk boundaries:

```python
# Feedback signal: when users copy part of a chunk, learn boundaries
copy_events = [(chunk, start_offset, end_offset) for ...]

# Train a boundary detector
# "Good chunks" = ones that get fully used
# "Bad chunks" = ones where user extracts a substring
```

### 5.5 Retrieval Caching with Staleness Detection

Cache query→results mappings, but invalidate intelligently:

```python
cache_entry = {
    "query_embedding": [...],
    "results": [...],
    "note_versions": {"note1.md": hash1, "note2.md": hash2},
    "timestamp": ...,
}

def is_stale(entry):
    # Invalidate if source notes changed
    for note, hash in entry.note_versions:
        if current_hash(note) != hash:
            return True
    return False
```

### 5.6 Attention Flow from LLM as Feedback

If using a local LLM, extract attention patterns:

```python
# Which retrieved chunks did the LLM attend to most?
attention_weights = get_cross_attention(llm, query, retrieved_chunks)

# Use as soft relevance labels
for chunk, weight in zip(retrieved_chunks, attention_weights):
    update_relevance(chunk, query, weight)
```

### 5.7 Predictive Pre-fetching

Based on current context, predict what you'll query next:

```python
def prefetch_candidates(current_session):
    # What notes are "adjacent" to current activity?
    recent_notes = current_session.accessed_notes[-5:]
    
    # Embed the session context
    session_embedding = mean([n.embedding for n in recent_notes])
    
    # Pre-compute similar notes
    prefetch = nearest_neighbors(session_embedding, k=50)
    cache(prefetch)
```

### 5.8 Episodic Memory Layer

Beyond semantic similarity, track **episodic associations**:

```python
# "I remember seeing something about X when I was working on Y"
episodic_index = {
    (time_window, activity_context): [accessed_notes]
}

def episodic_retrieval(query, current_context):
    similar_contexts = find_similar_contexts(current_context)
    episodic_candidates = [
        notes for ctx in similar_contexts 
        for notes in episodic_index[ctx]
    ]
    return episodic_candidates
```

---

## 6. Practical Implementation Recommendations

### Phase 1: Foundation (Week 1-2)

**Goal:** Basic RAG with logging infrastructure

```
1. Set up embedding pipeline
   - Model: gte-small or bge-small (local)
   - Chunking: 512 tokens with 50 token overlap
   - Storage: SQLite with sqlite-vss extension

2. Implement baseline retrieval
   - Hybrid: 0.7 * semantic + 0.3 * BM25
   - Top-k: 5 chunks

3. Build feedback logging
   - Log: query, retrieved_chunks, timestamps
   - Log: user actions (clicks, copies, expansions)
   - Format: append-only JSONL file
```

### Phase 2: Online Learning (Week 3-4)

**Goal:** Lightweight re-ranker that learns from implicit feedback

```
1. Define feature vector
   - Start with 5 features: semantic_sim, bm25, recency, 
     access_count, backlink_count

2. Implement online update
   - Learning rate: 0.01
   - Regularization: L2 with lambda=0.001
   - Update on every selection

3. A/B test against baseline
   - 50% of queries use learned ranker
   - Track click-through rate
```

### Phase 3: Structural Signals (Week 5-6)

**Goal:** Leverage Obsidian graph structure

```
1. Index backlinks and tags
   - Compute PageRank on link graph
   - Build tag co-occurrence matrix

2. Add structural features
   - pagerank_score
   - tag_overlap_with_query
   - folder_match

3. Implement exploration
   - Thompson sampling for uncertain chunks
   - Epsilon-greedy: 10% exploration
```

### Phase 4: Advanced Features (Month 2+)

**Goal:** Query understanding and retrieval specialization

```
1. Query intent classifier
   - Simple: keyword rules + embedding clustering
   - Classes: lookup, explore, synthesize, recent

2. Retrieval strategy per intent
   - Different k, diversity, recency weights

3. Query expansion
   - Use linked notes to expand queries
   - Extract key terms from related content

4. Periodic embedding adjustment
   - Weekly: fine-tune projection head on feedback
   - Monitor for degradation, auto-rollback
```

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Query Pipeline                          │
│                                                              │
│  Query → [Intent Classifier] → [Query Expander] → Expanded  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Retrieval Pipeline                        │
│                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │  Semantic   │    │    BM25     │    │  Episodic   │     │
│  │  Retrieval  │    │  Retrieval  │    │  Retrieval  │     │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘     │
│         └─────────────────┼─────────────────┘               │
│                           ▼                                  │
│                    [Candidate Pool]                          │
│                           │                                  │
└───────────────────────────┼─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Ranking Pipeline                          │
│                                                              │
│  Candidates → [Feature Extraction] → [Learned Re-ranker]    │
│                                            │                 │
│                                            ▼                 │
│                                     [Exploration Layer]      │
│                                            │                 │
│                                            ▼                 │
│                                      Final Ranking           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Feedback Loop                             │
│                                                              │
│  User Actions → [Implicit Signal Extraction] → Feedback Log │
│                                                         │    │
│  ┌───────────────────────────────────────────────────┐ │    │
│  │               Online Learner                       │◄┘    │
│  │  - Update re-ranker weights                       │       │
│  │  - Update chunk statistics                         │       │
│  │  - Update episodic memory                          │       │
│  └───────────────────────────────────────────────────┘       │
│                                                              │
│  ┌───────────────────────────────────────────────────┐       │
│  │            Periodic Batch Learner                  │       │
│  │  - Fine-tune embedding projection                  │       │
│  │  - Recompute chunk boundaries                      │       │
│  │  - Update intent classifier                        │       │
│  └───────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

### Key Files Structure

```
obsidian-rag/
├── core/
│   ├── embeddings.py       # Local embedding model wrapper
│   ├── retriever.py        # Hybrid semantic + BM25
│   ├── reranker.py         # Online learned re-ranker
│   └── chunker.py          # Markdown-aware chunking
├── learning/
│   ├── feedback_logger.py  # JSONL feedback logging
│   ├── online_learner.py   # Gradient descent updates
│   ├── explorer.py         # Thompson sampling
│   └── batch_trainer.py    # Periodic retraining
├── features/
│   ├── semantic.py         # Embedding similarity
│   ├── lexical.py          # BM25, term coverage
│   ├── structural.py       # PageRank, backlinks, tags
│   └── temporal.py         # Recency, access patterns
├── data/
│   ├── vectors.db          # SQLite with vector extension
│   ├── feedback.jsonl      # Append-only feedback log
│   ├── weights.json        # Learned re-ranker weights
│   └── projection.pt       # Learned embedding projection
└── config.yaml             # Retrieval parameters
```

### Metrics to Track

| Metric | Description | Target |
|--------|-------------|--------|
| **MRR@5** | Mean reciprocal rank of first relevant result | > 0.6 |
| **Click-through rate** | % of retrievals with user selection | > 40% |
| **Reformulation rate** | % of queries followed by refinement | < 20% |
| **Coverage** | % of vault accessible via retrieval | > 80% |
| **Latency p95** | 95th percentile response time | < 500ms |

---

## Conclusion

The most impactful investments for a personal knowledge RAG are:

1. **Implicit feedback collection** — This is your primary learning signal
2. **Lightweight online re-ranker** — Fast, interpretable, and effective
3. **Structural priors from Obsidian** — Free relevance signals you're probably ignoring
4. **Query intent awareness** — Different queries need different retrieval
5. **Exploration mechanisms** — Avoid local optima, surface forgotten knowledge

Avoid:
- Heavy neural re-ranker training (overkill for single-user)
- Explicit feedback as primary signal (too sparse)
- Fine-tuning full embedding models locally (unnecessary complexity)

The goal isn't a perfect system — it's a system that gets better every time you use it.

---

## References & Further Reading

- *Learning to Rank for Information Retrieval* — Liu (2011) — Foundational text on ranking
- *Multi-armed Bandits* — Slivkins (2019) — Exploration-exploitation theory
- *ColBERT* — Khattab & Zaharia — Late interaction for efficient re-ranking
- *BEIR Benchmark* — Thakur et al. — Zero-shot retrieval evaluation
- *RLHF for Retrieval* — Recent work on applying RLHF to improve retrievers
- *Contextual Bandits* — Excellent for personalization with feedback
- *Differential Privacy* — Dwork & Roth — Privacy-preserving ML fundamentals
