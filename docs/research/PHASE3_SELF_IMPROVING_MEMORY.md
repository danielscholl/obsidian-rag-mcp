# Phase 3 Research: Self-Improving Memory via Surprisal

**Status:** Research  
**Author:** Daniel Scholl
**Date:** 2026-02-14

---

## Executive Summary

This document explores how to make the RAG system learn and improve from usage. The core insight from cognitive science: memory works through **prediction + surprisal**. When predictions are wrong, the brain updates its model. We can apply this to RAG.

**Key Finding:** A hybrid approach combining lightweight implicit signals (click-through) with optional explicit feedback provides the best balance of user friction vs learning quality.

---

## 1. Background: Surprisal in Cognitive Science

### How Human Memory Works

Human memory isn't passive storage—it's an active prediction system:

1. **Prediction**: Brain predicts what information is relevant
2. **Comparison**: Compares prediction against actual outcome
3. **Surprisal**: Mismatch between expected and actual = learning signal
4. **Update**: Adjusts internal model to reduce future surprisal

**Key insight**: High surprisal events (unexpected corrections) carry the most information and drive the strongest learning.

### Application to RAG

Current RAG: Query → Retrieve → Return (static)

Self-improving RAG:
```
Query → Retrieve → Return → [User Feedback] → Update Model → Better Retrieval
                                    ↑
                              Surprisal signal
```

---

## 2. Feedback Mechanisms

### 2.1 Explicit Feedback

**What:** User directly rates results (thumbs up/down, stars, "was this helpful?")

**Pros:**
- Clear signal
- High information content
- User intent is unambiguous

**Cons:**
- High friction (users rarely provide feedback)
- Selection bias (only strong opinions recorded)
- Gaming/noise potential

**Examples:**
- Google search "feedback" button
- ChatGPT thumbs up/down
- Stack Overflow voting

### 2.2 Implicit Feedback

**What:** Infer relevance from user behavior

| Signal | Interpretation | Strength |
|--------|----------------|----------|
| Click-through | User found result interesting | Medium |
| Dwell time | Longer = more relevant | Medium |
| Copy/paste | User extracted value | High |
| Follow-up query | Original results insufficient | Negative |
| Query refinement | Partial success, needs tuning | Medium |
| No further queries | Satisfied (or gave up) | Ambiguous |

**Pros:**
- Zero friction
- Large volume of signals
- Natural behavior

**Cons:**
- Noisy (clicks ≠ relevance)
- Position bias (top results get more clicks)
- Requires interpretation

### 2.3 Correction-Based Learning

**What:** Learn from explicit corrections in conversation

```
User: "Find auth failures"
System: Returns token expiration RCAs
User: "No, I meant OAuth config issues"
       ↑
    Correction signal
```

**This is the highest-value signal** - it directly tells us:
1. What the user wanted
2. What we got wrong
3. How to fix it

**Challenge:** Detecting corrections automatically requires NLU.

---

## 3. What to Learn

### 3.1 Query-Result Associations

Store successful query → result mappings:

```json
{
  "query": "auth failures",
  "clicked_results": ["oauth-config-rca.md"],
  "skipped_results": ["token-expiration.md"],
  "timestamp": "2026-02-14T18:00:00Z"
}
```

Over time, boost results that get clicked for similar queries.

### 3.2 Conclusion Re-weighting

Adjust conclusion confidence based on utility:

```python
# Conclusion was useful → increase confidence
conclusion.confidence *= 1.1

# Conclusion was irrelevant → decrease confidence  
conclusion.confidence *= 0.9

# Conclusion was wrong → flag for review
conclusion.flagged = True
```

### 3.3 Query Expansion Rules

Learn synonyms and related terms from corrections:

```
"auth failures" → also search "OAuth", "authentication", "login issues"
```

### 3.4 Negative Examples

What NOT to return:

```json
{
  "query": "database issues",
  "negative_results": ["unrelated-networking-doc.md"],
  "reason": "user_correction"
}
```

---

## 4. Learning Algorithms

### 4.1 Simple Boosting

Lightweight, no ML required:

```python
def get_boost(result_id, query):
    # Count positive signals for this result on similar queries
    positive = count_clicks(result_id, similar_queries(query))
    negative = count_skips(result_id, similar_queries(query))
    
    if positive + negative == 0:
        return 1.0  # No data
    
    return 1.0 + (positive - negative) / (positive + negative) * 0.5
```

**Pros:** Simple, interpretable, fast  
**Cons:** Doesn't generalize well to new queries

### 4.2 Learning to Rank (LTR)

Train a model to re-rank results:

**Features:**
- Semantic similarity score
- BM25 score
- Click-through rate
- Recency
- Tag overlap
- Historical performance

**Models:**
- LambdaMART (gradient boosting)
- Neural LTR (transformer-based)
- Simple logistic regression

**Pros:** Generalizes better, handles multiple signals  
**Cons:** Needs training data, more complex

### 4.3 Bandit Approaches

Treat result ranking as multi-armed bandit:

- **Explore:** Occasionally show lower-ranked results to gather data
- **Exploit:** Show best-performing results most of the time

**Pros:** Balances learning vs performance  
**Cons:** May show suboptimal results during exploration

### 4.4 Embedding Fine-tuning

Fine-tune the embedding model on user feedback:

```python
# Positive pair: query and clicked result should be close
loss += distance(embed(query), embed(clicked_result))

# Negative pair: query and skipped result should be far
loss -= distance(embed(query), embed(skipped_result))
```

**Pros:** Improves core retrieval, not just re-ranking  
**Cons:** Expensive, needs significant data, risk of catastrophic forgetting

---

## 5. Architecture Options

### Option A: Feedback Store (Recommended for MVP)

```
┌─────────────────┐
│   User Query    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│  RAG Retrieval  │────▶│  Feedback Store │
└────────┬────────┘     │  (query→result  │
         │              │   mappings)     │
         ▼              └────────┬────────┘
┌─────────────────┐              │
│   Re-ranker     │◀─────────────┘
│ (boost by past  │
│  performance)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Results      │
└─────────────────┘
```

**Implementation:**
- SQLite or JSON file for feedback storage
- Simple boost calculation at query time
- No model training required

### Option B: Learning Pipeline

```
┌─────────────────┐
│ Feedback Events │
└────────┬────────┘
         │ (async)
         ▼
┌─────────────────┐
│  Training Job   │
│  (periodic)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Ranking Model  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  RAG + Re-rank  │
└─────────────────┘
```

**Implementation:**
- Batch training on accumulated feedback
- Deploy updated model periodically
- More complex but more powerful

### Option C: Online Learning

```
Query → Retrieve → Return → Feedback → Immediate Update
                                              │
                                              ▼
                                    ┌─────────────────┐
                                    │  Model Update   │
                                    │  (incremental)  │
                                    └─────────────────┘
```

**Implementation:**
- Update model after each interaction
- Requires careful learning rate tuning
- Risk of instability

---

## 6. Data Schema

### Feedback Event

```json
{
  "id": "evt_123",
  "timestamp": "2026-02-14T18:30:00Z",
  "session_id": "sess_456",
  "query": "database connection issues",
  "query_embedding": [0.1, 0.2, ...],
  "results_shown": [
    {"id": "doc1:0", "position": 1, "score": 0.85},
    {"id": "doc2:0", "position": 2, "score": 0.72}
  ],
  "interactions": [
    {"type": "click", "result_id": "doc1:0", "dwell_ms": 45000},
    {"type": "copy", "result_id": "doc1:0"}
  ],
  "explicit_feedback": null,
  "correction": null
}
```

### Correction Event

```json
{
  "id": "corr_789",
  "timestamp": "2026-02-14T18:31:00Z",
  "original_query": "auth failures", 
  "original_results": ["token-rca.md", "session-rca.md"],
  "correction_text": "I meant OAuth config issues",
  "correct_result": "oauth-config-rca.md",
  "learned_association": {
    "query_terms": ["auth", "failures"],
    "should_include": ["oauth", "config"],
    "should_exclude": ["token", "session"]
  }
}
```

### Result Performance

```json
{
  "result_id": "doc1:0",
  "total_impressions": 150,
  "total_clicks": 45,
  "ctr": 0.30,
  "avg_dwell_ms": 32000,
  "positive_feedback": 12,
  "negative_feedback": 2,
  "queries_clicked_from": ["database issues", "connection pool", "timeout"],
  "last_updated": "2026-02-14T18:30:00Z"
}
```

---

## 7. Privacy Considerations

### What We Store

| Data | Privacy Risk | Mitigation |
|------|--------------|------------|
| Queries | Medium (may contain sensitive info) | Hash or encrypt, retention limits |
| Click data | Low | Aggregate, don't store user IDs |
| Corrections | Medium | User consent, local-only option |
| Embeddings | Low (not human-readable) | None needed |

### Recommendations

1. **Local-first**: All feedback stored locally by default
2. **Opt-in sharing**: Optional anonymized feedback for improvement
3. **Retention limits**: Auto-delete feedback older than N days
4. **No PII**: Never store user identifiers with feedback

---

## 8. Proposal: MVP Implementation

### Phase 3a: Implicit Feedback (Low Effort)

**Scope:**
- Track which results are returned
- Track which results user queries further about
- Simple boost for frequently-accessed results

**Implementation:**
- Add `feedback_store.py` module
- Log result impressions
- Boost calculation in re-ranking

**Effort:** 2-3 days

### Phase 3b: Explicit Feedback (Medium Effort)

**Scope:**
- Add feedback API to MCP tools
- "Was this helpful?" in results
- Store and apply feedback

**Implementation:**
- New MCP tool: `submit_feedback`
- Feedback storage and retrieval
- Boost/penalty based on feedback

**Effort:** 3-5 days

### Phase 3c: Correction Learning (Higher Effort)

**Scope:**
- Detect corrections in conversation
- Extract what user actually wanted
- Build query expansion rules

**Implementation:**
- NLU for correction detection
- Association learning
- Query rewriting

**Effort:** 1-2 weeks

---

## 9. Success Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Precision@3 | Relevant results in top 3 | +10% over baseline |
| Click-through rate | Users clicking results | +15% over baseline |
| Query refinement rate | Users needing to rephrase | -20% from baseline |
| Time to answer | How fast users find what they need | -25% from baseline |

---

## 10. Open Questions

1. **How much feedback is enough?** 
   - Minimum viable dataset for learning?
   - Cold start problem for new vaults?

2. **How to handle concept drift?**
   - User needs change over time
   - Old feedback may become stale

3. **Multi-user scenarios?**
   - Should feedback be per-user or shared?
   - Privacy vs collective learning tradeoff

4. **Evaluation without ground truth?**
   - No labeled "correct" results
   - A/B testing feasibility?

---

## 11. Recommendations

### Start With: Phase 3a (Implicit Feedback)

**Why:**
- Zero user friction
- Provides baseline data
- Low implementation cost
- Can always add explicit feedback later

### Next: Phase 3b (Explicit Feedback)

**Why:**
- Higher signal quality
- Complements implicit data
- Users who care can help improve

### Future: Phase 3c (Corrections)

**Why:**
- Highest value learning
- Requires more sophisticated NLU
- Best saved for when we have usage data

---

## References

1. Friston, K. (2010). "The free-energy principle: a unified brain theory?"
2. Rao, R. & Ballard, D. (1999). "Predictive coding in the visual cortex"
3. Liu, T. (2009). "Learning to Rank for Information Retrieval"
4. Joachims, T. (2002). "Optimizing Search Engines using Clickthrough Data"
5. Radlinski, F. & Joachims, T. (2005). "Query Chains: Learning to Rank from Implicit Feedback"
