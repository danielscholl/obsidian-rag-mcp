---
title: "2025-06-10 - Deadlock in Transaction in auth-service"
date: 2025-06-10
severity: P2
services: [auth-service, analytics-pipeline]
tags: [rca, p2, database]
status: resolved
duration_minutes: 144
author: DevOps
---

# 2025-06-10 - Deadlock in Transaction in auth-service

## Summary

On 2025-06-10, the auth-service service experienced a deadlock in transaction in SQL Server. The incident lasted approximately 144 minutes and affected 7610 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 14:26 | Monitoring alert triggered |
| 14:28 | On-call engineer paged |
| 14:31 | Initial investigation started |
| 14:36 | Root cause identified |
| 15:52 | Mitigation applied |
| 16:21 | Service recovery observed |
| 16:50 | Incident resolved |

## Root Cause


The root cause was traced to SQL Server connection handling. Under increased load from a marketing campaign, the connection pool (128 connections) became exhausted.

Key factors:
1. Connection timeout was set to 37 seconds, too long for our use case
2. No connection pool monitoring was in place
3. The service was holding connections during long-running operations

Technical details:
```
Error: SQL ServerException: Connection pool exhausted
Max pool size: 172
Active connections: 215
Waiting requests: 264
```


## Impact


- Service degradation: 70% of requests affected
- Error rate spike: 19% (baseline: <1%)
- Latency increase: p99 went from 314ms to 3408ms


### Affected Services
- auth-service
- analytics-pipeline

### Customer Impact

- 4675 customer-facing errors
- 68 support tickets created
- Estimated revenue impact: $39987


## Resolution


1. Increased connection pool size from 96 to 356
2. Reduced connection timeout from 99s to 27s  
3. Implemented connection pooling best practices
4. Added circuit breaker pattern for SQL Server calls


## Lessons Learned

### What Went Well

- Alert fired within 3 minutes of incident start
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
| P1 | Implement monitoring for deadlock in transaction | Backend Team | 2025-06-17 |
| P2 | Update runbook | Backend Team | 2025-06-24 |
| P2 | Add load test scenario | SRE | 2025-07-01 |
| P3 | Review similar services | Database Team | 2025-07-10 |


## Related Incidents


- [[2025-06-10-previous-incident|Previous database incident]]
- [[runbook-auth-service|auth-service Runbook]]
- [[architecture-database|Database Architecture]]


---
*RCA prepared by DevOps on 2025-06-14*
