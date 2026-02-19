---
title: "2025-02-24 - Database Connection Pool Exhaustion in analytics-pipeline"
date: 2025-02-24
severity: P1
services: [analytics-pipeline, recommendation-engine, user-service, billing-api]
tags: [rca, p1, database]
status: resolved
duration_minutes: 128
author: SRE
---

# 2025-02-24 - Database Connection Pool Exhaustion in analytics-pipeline

## Summary

On 2025-02-24, the analytics-pipeline service experienced a database connection pool exhaustion in PostgreSQL. The incident lasted approximately 128 minutes and affected 2568 users and 4 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 22:03 | Monitoring alert triggered |
| 22:05 | On-call engineer paged |
| 22:08 | Initial investigation started |
| 22:13 | Root cause identified |
| 23:19 | Mitigation applied |
| 23:45 | Service recovery observed |
| 00:11 | Incident resolved |

## Root Cause


The root cause was traced to PostgreSQL connection handling. Under increased load from a marketing campaign, the connection pool (117 connections) became exhausted.

Key factors:
1. Connection timeout was set to 117 seconds, too long for our use case
2. No connection pool monitoring was in place
3. The service was holding connections during long-running operations

Technical details:
```
Error: PostgreSQLException: Connection pool exhausted
Max pool size: 81
Active connections: 257
Waiting requests: 801
```


## Impact


- Service degradation: 59% of requests affected
- Error rate spike: 48% (baseline: <1%)
- Latency increase: p99 went from 263ms to 2229ms


### Affected Services
- analytics-pipeline
- recommendation-engine
- user-service
- billing-api

### Customer Impact

- 1999 customer-facing errors
- 79 support tickets created
- Estimated revenue impact: $12312


## Resolution


1. Increased connection pool size from 98 to 208
2. Reduced connection timeout from 94s to 16s  
3. Implemented connection pooling best practices
4. Added circuit breaker pattern for PostgreSQL calls


## Lessons Learned

### What Went Well

- Alert fired within 3 minutes of incident start
- On-call response was quick (2 minutes)
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
| P1 | Implement monitoring for database connection pool exhaustion | Infrastructure | 2025-03-03 |
| P2 | Update runbook | Infrastructure | 2025-03-10 |
| P2 | Add load test scenario | SRE | 2025-03-17 |
| P3 | Review similar services | DevOps | 2025-03-26 |


## Related Incidents


- [[2025-02-24-previous-incident|Previous database incident]]
- [[runbook-analytics-pipeline|analytics-pipeline Runbook]]
- [[architecture-database|Database Architecture]]


---
*RCA prepared by SRE on 2025-02-28*
