---
title: "2025-05-04 - Deadlock in Transaction in recommendation-engine"
date: 2025-05-04
severity: P2
services: [recommendation-engine, inventory-api]
tags: [rca, p2, database]
status: resolved
duration_minutes: 51
author: DevOps
---

# 2025-05-04 - Deadlock in Transaction in recommendation-engine

## Summary

On 2025-05-04, the recommendation-engine service experienced a deadlock in transaction in PostgreSQL. The incident lasted approximately 51 minutes and affected 9953 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 08:17 | Monitoring alert triggered |
| 08:19 | On-call engineer paged |
| 08:22 | Initial investigation started |
| 08:27 | Root cause identified |
| 08:47 | Mitigation applied |
| 08:57 | Service recovery observed |
| 09:08 | Incident resolved |

## Root Cause


The root cause was traced to PostgreSQL connection handling. Under increased load from a marketing campaign, the connection pool (56 connections) became exhausted.

Key factors:
1. Connection timeout was set to 75 seconds, too long for our use case
2. No connection pool monitoring was in place
3. The service was holding connections during long-running operations

Technical details:
```
Error: PostgreSQLException: Connection pool exhausted
Max pool size: 55
Active connections: 253
Waiting requests: 866
```


## Impact


- Service degradation: 100% of requests affected
- Error rate spike: 24% (baseline: <1%)
- Latency increase: p99 went from 128ms to 5814ms


### Affected Services
- recommendation-engine
- inventory-api

### Customer Impact

- 1187 customer-facing errors
- 82 support tickets created
- Estimated revenue impact: $17370


## Resolution


1. Increased connection pool size from 82 to 495
2. Reduced connection timeout from 92s to 18s  
3. Implemented connection pooling best practices
4. Added circuit breaker pattern for PostgreSQL calls


## Lessons Learned

### What Went Well

- Alert fired within 2 minutes of incident start
- On-call response was quick (10 minutes)
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
| P1 | Implement monitoring for deadlock in transaction | Database Team | 2025-05-11 |
| P2 | Update runbook | Database Team | 2025-05-18 |
| P2 | Add load test scenario | SRE | 2025-05-25 |
| P3 | Review similar services | Infrastructure | 2025-06-03 |


## Related Incidents


- [[2025-05-04-previous-incident|Previous database incident]]
- [[runbook-recommendation-engine|recommendation-engine Runbook]]
- [[architecture-database|Database Architecture]]


---
*RCA prepared by DevOps on 2025-05-05*
