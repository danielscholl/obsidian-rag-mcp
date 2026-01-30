---
title: "2026-01-10 - Deadlock in Transaction in search-api"
date: 2026-01-10
severity: P2
services: [search-api, recommendation-engine]
tags: [rca, p2, database]
status: resolved
duration_minutes: 42
author: Backend Team
---

# 2026-01-10 - Deadlock in Transaction in search-api

## Summary

On 2026-01-10, the search-api service experienced a deadlock in transaction in MongoDB. The incident lasted approximately 42 minutes and affected 9333 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 13:16 | Monitoring alert triggered |
| 13:18 | On-call engineer paged |
| 13:21 | Initial investigation started |
| 13:26 | Root cause identified |
| 13:41 | Mitigation applied |
| 13:49 | Service recovery observed |
| 13:58 | Incident resolved |

## Root Cause


The root cause was traced to MongoDB connection handling. Under increased load from a marketing campaign, the connection pool (139 connections) became exhausted.

Key factors:
1. Connection timeout was set to 68 seconds, too long for our use case
2. No connection pool monitoring was in place
3. The service was holding connections during long-running operations

Technical details:
```
Error: MongoDBException: Connection pool exhausted
Max pool size: 63
Active connections: 445
Waiting requests: 169
```


## Impact


- Service degradation: 63% of requests affected
- Error rate spike: 17% (baseline: <1%)
- Latency increase: p99 went from 149ms to 2609ms


### Affected Services
- search-api
- recommendation-engine

### Customer Impact

- 2838 customer-facing errors
- 97 support tickets created
- Estimated revenue impact: $33742


## Resolution


1. Increased connection pool size from 90 to 344
2. Reduced connection timeout from 67s to 20s  
3. Implemented connection pooling best practices
4. Added circuit breaker pattern for MongoDB calls


## Lessons Learned

### What Went Well

- Alert fired within 5 minutes of incident start
- On-call response was quick (5 minutes)
- Cross-team collaboration was effective
- Communication to stakeholders was timely


### What Could Be Improved  

- Need better runbooks for database issues
- Monitoring coverage gaps identified
- Load testing should cover this scenario
- Need automated rollback for faster recovery


## Action Items


| Priority | Action | Owner | Due Date |
|----------|--------|-------|----------|
| P1 | Implement monitoring for deadlock in transaction | DevOps | 2026-01-17 |
| P2 | Update runbook | DevOps | 2026-01-24 |
| P2 | Add load test scenario | Platform Engineering | 2026-01-31 |
| P3 | Review similar services | Infrastructure | 2026-02-09 |


## Related Incidents


- [[2026-01-10-previous-incident|Previous database incident]]
- [[runbook-search-api|search-api Runbook]]
- [[architecture-database|Database Architecture]]


---
*RCA prepared by Backend Team on 2026-01-14*
