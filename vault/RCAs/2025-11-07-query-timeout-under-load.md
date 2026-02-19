---
title: "2025-11-07 - Query Timeout Under Load in auth-service"
date: 2025-11-07
severity: P2
services: [auth-service, order-service, notification-service, user-service]
tags: [rca, p2, database]
status: resolved
duration_minutes: 135
author: DevOps
---

# 2025-11-07 - Query Timeout Under Load in auth-service

## Summary

On 2025-11-07, the auth-service service experienced a query timeout under load in PostgreSQL. The incident lasted approximately 135 minutes and affected 2044 users and 4 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 03:43 | Monitoring alert triggered |
| 03:45 | On-call engineer paged |
| 03:48 | Initial investigation started |
| 03:53 | Root cause identified |
| 05:04 | Mitigation applied |
| 05:31 | Service recovery observed |
| 05:58 | Incident resolved |

## Root Cause


The root cause was traced to PostgreSQL connection handling. Under increased load from a marketing campaign, the connection pool (140 connections) became exhausted.

Key factors:
1. Connection timeout was set to 112 seconds, too long for our use case
2. No connection pool monitoring was in place
3. The service was holding connections during long-running operations

Technical details:
```
Error: PostgreSQLException: Connection pool exhausted
Max pool size: 137
Active connections: 320
Waiting requests: 414
```


## Impact


- Service degradation: 100% of requests affected
- Error rate spike: 40% (baseline: <1%)
- Latency increase: p99 went from 198ms to 8466ms


### Affected Services
- auth-service
- order-service
- notification-service
- user-service

### Customer Impact

- 138 customer-facing errors
- 82 support tickets created
- Estimated revenue impact: $10484


## Resolution


1. Increased connection pool size from 55 to 439
2. Reduced connection timeout from 68s to 10s  
3. Implemented connection pooling best practices
4. Added circuit breaker pattern for PostgreSQL calls


## Lessons Learned

### What Went Well

- Alert fired within 5 minutes of incident start
- On-call response was quick (4 minutes)
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
| P1 | Implement monitoring for query timeout under load | DevOps | 2025-11-14 |
| P2 | Update runbook | Platform Engineering | 2025-11-21 |
| P2 | Add load test scenario | DevOps | 2025-11-28 |
| P3 | Review similar services | Infrastructure | 2025-12-07 |


## Related Incidents


- [[2025-11-07-previous-incident|Previous database incident]]
- [[runbook-auth-service|auth-service Runbook]]
- [[architecture-database|Database Architecture]]


---
*RCA prepared by DevOps on 2025-11-12*
