---
title: "2026-01-06 - Deadlock in Transaction in auth-service"
date: 2026-01-06
severity: P2
services: [auth-service, inventory-api]
tags: [rca, p2, database]
status: resolved
duration_minutes: 129
author: DevOps
---

# 2026-01-06 - Deadlock in Transaction in auth-service

## Summary

On 2026-01-06, the auth-service service experienced a deadlock in transaction in SQL Server. The incident lasted approximately 129 minutes and affected 2174 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 21:24 | Monitoring alert triggered |
| 21:26 | On-call engineer paged |
| 21:29 | Initial investigation started |
| 21:34 | Root cause identified |
| 22:41 | Mitigation applied |
| 23:07 | Service recovery observed |
| 23:33 | Incident resolved |

## Root Cause


The root cause was traced to SQL Server connection handling. Under increased load from a marketing campaign, the connection pool (117 connections) became exhausted.

Key factors:
1. Connection timeout was set to 63 seconds, too long for our use case
2. No connection pool monitoring was in place
3. The service was holding connections during long-running operations

Technical details:
```
Error: SQL ServerException: Connection pool exhausted
Max pool size: 114
Active connections: 485
Waiting requests: 977
```


## Impact


- Service degradation: 75% of requests affected
- Error rate spike: 33% (baseline: <1%)
- Latency increase: p99 went from 432ms to 7098ms


### Affected Services
- auth-service
- inventory-api

### Customer Impact

- 2757 customer-facing errors
- 37 support tickets created
- Estimated revenue impact: $37133


## Resolution


1. Increased connection pool size from 95 to 377
2. Reduced connection timeout from 86s to 27s  
3. Implemented connection pooling best practices
4. Added circuit breaker pattern for SQL Server calls


## Lessons Learned

### What Went Well

- Alert fired within 1 minutes of incident start
- On-call response was quick (8 minutes)
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
| P1 | Implement monitoring for deadlock in transaction | DevOps | 2026-01-13 |
| P2 | Update runbook | Platform Engineering | 2026-01-20 |
| P2 | Add load test scenario | Backend Team | 2026-01-27 |
| P3 | Review similar services | Platform Engineering | 2026-02-05 |


## Related Incidents


- [[2026-01-06-previous-incident|Previous database incident]]
- [[runbook-auth-service|auth-service Runbook]]
- [[architecture-database|Database Architecture]]


---
*RCA prepared by DevOps on 2026-01-11*
