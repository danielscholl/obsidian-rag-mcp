---
title: "2025-12-25 - Database Connection Pool Exhaustion in auth-service"
date: 2025-12-25
severity: P1
services: [auth-service, order-service, analytics-pipeline]
tags: [rca, p1, database]
status: resolved
duration_minutes: 49
author: Platform Engineering
---

# 2025-12-25 - Database Connection Pool Exhaustion in auth-service

## Summary

On 2025-12-25, the auth-service service experienced a database connection pool exhaustion in CosmosDB. The incident lasted approximately 49 minutes and affected 7971 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 08:41 | Monitoring alert triggered |
| 08:43 | On-call engineer paged |
| 08:46 | Initial investigation started |
| 08:51 | Root cause identified |
| 09:10 | Mitigation applied |
| 09:20 | Service recovery observed |
| 09:30 | Incident resolved |

## Root Cause


The root cause was traced to CosmosDB connection handling. Under increased load from a marketing campaign, the connection pool (56 connections) became exhausted.

Key factors:
1. Connection timeout was set to 31 seconds, too long for our use case
2. No connection pool monitoring was in place
3. The service was holding connections during long-running operations

Technical details:
```
Error: CosmosDBException: Connection pool exhausted
Max pool size: 52
Active connections: 241
Waiting requests: 891
```


## Impact


- Service degradation: 78% of requests affected
- Error rate spike: 42% (baseline: <1%)
- Latency increase: p99 went from 491ms to 5809ms


### Affected Services
- auth-service
- order-service
- analytics-pipeline

### Customer Impact

- 1732 customer-facing errors
- 43 support tickets created
- Estimated revenue impact: $28033


## Resolution


1. Increased connection pool size from 61 to 361
2. Reduced connection timeout from 68s to 12s  
3. Implemented connection pooling best practices
4. Added circuit breaker pattern for CosmosDB calls


## Lessons Learned

### What Went Well

- Alert fired within 1 minutes of incident start
- On-call response was quick (6 minutes)
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
| P1 | Implement monitoring for database connection pool exhaustion | DevOps | 2026-01-01 |
| P2 | Update runbook | SRE | 2026-01-08 |
| P2 | Add load test scenario | Platform Engineering | 2026-01-15 |
| P3 | Review similar services | Platform Engineering | 2026-01-24 |


## Related Incidents


- [[2025-12-25-previous-incident|Previous database incident]]
- [[runbook-auth-service|auth-service Runbook]]
- [[architecture-database|Database Architecture]]


---
*RCA prepared by Platform Engineering on 2025-12-28*
