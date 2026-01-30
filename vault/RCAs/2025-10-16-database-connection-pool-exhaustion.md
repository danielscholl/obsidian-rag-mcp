---
title: "2025-10-16 - Database Connection Pool Exhaustion in inventory-api"
date: 2025-10-16
severity: P1
services: [inventory-api, user-service, payment-gateway]
tags: [rca, p1, database]
status: resolved
duration_minutes: 123
author: DevOps
---

# 2025-10-16 - Database Connection Pool Exhaustion in inventory-api

## Summary

On 2025-10-16, the inventory-api service experienced a database connection pool exhaustion in PostgreSQL. The incident lasted approximately 123 minutes and affected 9555 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 23:45 | Monitoring alert triggered |
| 23:47 | On-call engineer paged |
| 23:50 | Initial investigation started |
| 23:55 | Root cause identified |
| 00:58 | Mitigation applied |
| 01:23 | Service recovery observed |
| 01:48 | Incident resolved |

## Root Cause


The root cause was traced to PostgreSQL connection handling. Under increased load from a marketing campaign, the connection pool (61 connections) became exhausted.

Key factors:
1. Connection timeout was set to 99 seconds, too long for our use case
2. No connection pool monitoring was in place
3. The service was holding connections during long-running operations

Technical details:
```
Error: PostgreSQLException: Connection pool exhausted
Max pool size: 150
Active connections: 345
Waiting requests: 722
```


## Impact


- Service degradation: 86% of requests affected
- Error rate spike: 40% (baseline: <1%)
- Latency increase: p99 went from 349ms to 8046ms


### Affected Services
- inventory-api
- user-service
- payment-gateway

### Customer Impact

- 1681 customer-facing errors
- 28 support tickets created
- Estimated revenue impact: $19746


## Resolution


1. Increased connection pool size from 63 to 324
2. Reduced connection timeout from 103s to 15s  
3. Implemented connection pooling best practices
4. Added circuit breaker pattern for PostgreSQL calls


## Lessons Learned

### What Went Well

- Alert fired within 1 minutes of incident start
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
| P1 | Implement monitoring for database connection pool exhaustion | Database Team | 2025-10-23 |
| P2 | Update runbook | DevOps | 2025-10-30 |
| P2 | Add load test scenario | DevOps | 2025-11-06 |
| P3 | Review similar services | Database Team | 2025-11-15 |


## Related Incidents


- [[2025-10-16-previous-incident|Previous database incident]]
- [[runbook-inventory-api|inventory-api Runbook]]
- [[architecture-database|Database Architecture]]


---
*RCA prepared by DevOps on 2025-10-20*
