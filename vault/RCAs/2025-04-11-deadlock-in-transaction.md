---
title: "2025-04-11 - Deadlock in Transaction in billing-api"
date: 2025-04-11
severity: P2
services: [billing-api, search-api, analytics-pipeline, user-service]
tags: [rca, p2, database]
status: resolved
duration_minutes: 109
author: Platform Engineering
---

# 2025-04-11 - Deadlock in Transaction in billing-api

## Summary

On 2025-04-11, the billing-api service experienced a deadlock in transaction in SQL Server. The incident lasted approximately 109 minutes and affected 9038 users and 4 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 06:06 | Monitoring alert triggered |
| 06:08 | On-call engineer paged |
| 06:11 | Initial investigation started |
| 06:16 | Root cause identified |
| 07:11 | Mitigation applied |
| 07:33 | Service recovery observed |
| 07:55 | Incident resolved |

## Root Cause


The root cause was traced to SQL Server connection handling. Under increased load from a marketing campaign, the connection pool (84 connections) became exhausted.

Key factors:
1. Connection timeout was set to 37 seconds, too long for our use case
2. No connection pool monitoring was in place
3. The service was holding connections during long-running operations

Technical details:
```
Error: SQL ServerException: Connection pool exhausted
Max pool size: 91
Active connections: 368
Waiting requests: 947
```


## Impact


- Service degradation: 94% of requests affected
- Error rate spike: 35% (baseline: <1%)
- Latency increase: p99 went from 425ms to 8475ms


### Affected Services
- billing-api
- search-api
- analytics-pipeline
- user-service

### Customer Impact

- 1357 customer-facing errors
- 87 support tickets created
- Estimated revenue impact: $40424


## Resolution


1. Increased connection pool size from 87 to 386
2. Reduced connection timeout from 112s to 23s  
3. Implemented connection pooling best practices
4. Added circuit breaker pattern for SQL Server calls


## Lessons Learned

### What Went Well

- Alert fired within 2 minutes of incident start
- On-call response was quick (3 minutes)
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
| P1 | Implement monitoring for deadlock in transaction | DevOps | 2025-04-18 |
| P2 | Update runbook | SRE | 2025-04-25 |
| P2 | Add load test scenario | Infrastructure | 2025-05-02 |
| P3 | Review similar services | DevOps | 2025-05-11 |


## Related Incidents


- [[2025-04-11-previous-incident|Previous database incident]]
- [[runbook-billing-api|billing-api Runbook]]
- [[architecture-database|Database Architecture]]


---
*RCA prepared by Platform Engineering on 2025-04-14*
