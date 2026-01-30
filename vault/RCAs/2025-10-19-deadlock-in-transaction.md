---
title: "2025-10-19 - Deadlock in Transaction in inventory-api"
date: 2025-10-19
severity: P2
services: [inventory-api, billing-api, search-api, user-service]
tags: [rca, p2, database]
status: resolved
duration_minutes: 42
author: Backend Team
---

# 2025-10-19 - Deadlock in Transaction in inventory-api

## Summary

On 2025-10-19, the inventory-api service experienced a deadlock in transaction in PostgreSQL. The incident lasted approximately 42 minutes and affected 708 users and 4 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 03:22 | Monitoring alert triggered |
| 03:24 | On-call engineer paged |
| 03:27 | Initial investigation started |
| 03:32 | Root cause identified |
| 03:47 | Mitigation applied |
| 03:55 | Service recovery observed |
| 04:04 | Incident resolved |

## Root Cause


The root cause was traced to PostgreSQL connection handling. Under increased load from a marketing campaign, the connection pool (89 connections) became exhausted.

Key factors:
1. Connection timeout was set to 119 seconds, too long for our use case
2. No connection pool monitoring was in place
3. The service was holding connections during long-running operations

Technical details:
```
Error: PostgreSQLException: Connection pool exhausted
Max pool size: 76
Active connections: 272
Waiting requests: 388
```


## Impact


- Service degradation: 88% of requests affected
- Error rate spike: 47% (baseline: <1%)
- Latency increase: p99 went from 398ms to 9988ms


### Affected Services
- inventory-api
- billing-api
- search-api
- user-service

### Customer Impact

- 3901 customer-facing errors
- 25 support tickets created
- Estimated revenue impact: $47696


## Resolution


1. Increased connection pool size from 58 to 223
2. Reduced connection timeout from 110s to 28s  
3. Implemented connection pooling best practices
4. Added circuit breaker pattern for PostgreSQL calls


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
| P1 | Implement monitoring for deadlock in transaction | SRE | 2025-10-26 |
| P2 | Update runbook | SRE | 2025-11-02 |
| P2 | Add load test scenario | Platform Engineering | 2025-11-09 |
| P3 | Review similar services | Database Team | 2025-11-18 |


## Related Incidents


- [[2025-10-19-previous-incident|Previous database incident]]
- [[runbook-inventory-api|inventory-api Runbook]]
- [[architecture-database|Database Architecture]]


---
*RCA prepared by Backend Team on 2025-10-23*
