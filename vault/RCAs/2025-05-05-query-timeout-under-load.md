---
title: "2025-05-05 - Query Timeout Under Load in user-service"
date: 2025-05-05
severity: P2
services: [user-service, billing-api, notification-service]
tags: [rca, p2, database]
status: resolved
duration_minutes: 65
author: Platform Engineering
---

# 2025-05-05 - Query Timeout Under Load in user-service

## Summary

On 2025-05-05, the user-service service experienced a query timeout under load in SQL Server. The incident lasted approximately 65 minutes and affected 6650 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 22:00 | Monitoring alert triggered |
| 22:02 | On-call engineer paged |
| 22:05 | Initial investigation started |
| 22:10 | Root cause identified |
| 22:39 | Mitigation applied |
| 22:52 | Service recovery observed |
| 23:05 | Incident resolved |

## Root Cause


The root cause was traced to SQL Server connection handling. Under increased load from a marketing campaign, the connection pool (107 connections) became exhausted.

Key factors:
1. Connection timeout was set to 69 seconds, too long for our use case
2. No connection pool monitoring was in place
3. The service was holding connections during long-running operations

Technical details:
```
Error: SQL ServerException: Connection pool exhausted
Max pool size: 192
Active connections: 229
Waiting requests: 101
```


## Impact


- Service degradation: 53% of requests affected
- Error rate spike: 18% (baseline: <1%)
- Latency increase: p99 went from 369ms to 8595ms


### Affected Services
- user-service
- billing-api
- notification-service

### Customer Impact

- 1416 customer-facing errors
- 20 support tickets created
- Estimated revenue impact: $3960


## Resolution


1. Increased connection pool size from 94 to 376
2. Reduced connection timeout from 119s to 26s  
3. Implemented connection pooling best practices
4. Added circuit breaker pattern for SQL Server calls


## Lessons Learned

### What Went Well

- Alert fired within 2 minutes of incident start
- On-call response was quick (7 minutes)
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
| P1 | Implement monitoring for query timeout under load | Infrastructure | 2025-05-12 |
| P2 | Update runbook | Backend Team | 2025-05-19 |
| P2 | Add load test scenario | DevOps | 2025-05-26 |
| P3 | Review similar services | Infrastructure | 2025-06-04 |


## Related Incidents


- [[2025-05-05-previous-incident|Previous database incident]]
- [[runbook-user-service|user-service Runbook]]
- [[architecture-database|Database Architecture]]


---
*RCA prepared by Platform Engineering on 2025-05-07*
