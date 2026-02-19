---
title: "2025-03-05 - Database Connection Pool Exhaustion in order-service"
date: 2025-03-05
severity: P1
services: [order-service, billing-api, search-api, inventory-api]
tags: [rca, p1, database]
status: resolved
duration_minutes: 75
author: Backend Team
---

# 2025-03-05 - Database Connection Pool Exhaustion in order-service

## Summary

On 2025-03-05, the order-service service experienced a database connection pool exhaustion in SQL Server. The incident lasted approximately 75 minutes and affected 3138 users and 4 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 18:25 | Monitoring alert triggered |
| 18:27 | On-call engineer paged |
| 18:30 | Initial investigation started |
| 18:35 | Root cause identified |
| 19:10 | Mitigation applied |
| 19:25 | Service recovery observed |
| 19:40 | Incident resolved |

## Root Cause


The root cause was traced to SQL Server connection handling. Under increased load from a marketing campaign, the connection pool (149 connections) became exhausted.

Key factors:
1. Connection timeout was set to 60 seconds, too long for our use case
2. No connection pool monitoring was in place
3. The service was holding connections during long-running operations

Technical details:
```
Error: SQL ServerException: Connection pool exhausted
Max pool size: 88
Active connections: 342
Waiting requests: 864
```


## Impact


- Service degradation: 91% of requests affected
- Error rate spike: 18% (baseline: <1%)
- Latency increase: p99 went from 196ms to 9782ms


### Affected Services
- order-service
- billing-api
- search-api
- inventory-api

### Customer Impact

- 511 customer-facing errors
- 61 support tickets created
- Estimated revenue impact: $20048


## Resolution


1. Increased connection pool size from 66 to 433
2. Reduced connection timeout from 89s to 28s  
3. Implemented connection pooling best practices
4. Added circuit breaker pattern for SQL Server calls


## Lessons Learned

### What Went Well

- Alert fired within 3 minutes of incident start
- On-call response was quick (9 minutes)
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
| P1 | Implement monitoring for database connection pool exhaustion | DevOps | 2025-03-12 |
| P2 | Update runbook | Infrastructure | 2025-03-19 |
| P2 | Add load test scenario | Backend Team | 2025-03-26 |
| P3 | Review similar services | SRE | 2025-04-04 |


## Related Incidents


- [[2025-03-05-previous-incident|Previous database incident]]
- [[runbook-order-service|order-service Runbook]]
- [[architecture-database|Database Architecture]]


---
*RCA prepared by Backend Team on 2025-03-06*
