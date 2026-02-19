---
title: "2025-08-27 - Deadlock in Transaction in user-service"
date: 2025-08-27
severity: P2
services: [user-service, billing-api, payment-gateway]
tags: [rca, p2, database]
status: resolved
duration_minutes: 146
author: Backend Team
---

# 2025-08-27 - Deadlock in Transaction in user-service

## Summary

On 2025-08-27, the user-service service experienced a deadlock in transaction in MongoDB. The incident lasted approximately 146 minutes and affected 7557 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 07:25 | Monitoring alert triggered |
| 07:27 | On-call engineer paged |
| 07:30 | Initial investigation started |
| 07:35 | Root cause identified |
| 08:52 | Mitigation applied |
| 09:21 | Service recovery observed |
| 09:51 | Incident resolved |

## Root Cause


The root cause was traced to MongoDB connection handling. Under increased load from a marketing campaign, the connection pool (108 connections) became exhausted.

Key factors:
1. Connection timeout was set to 120 seconds, too long for our use case
2. No connection pool monitoring was in place
3. The service was holding connections during long-running operations

Technical details:
```
Error: MongoDBException: Connection pool exhausted
Max pool size: 61
Active connections: 313
Waiting requests: 628
```


## Impact


- Service degradation: 72% of requests affected
- Error rate spike: 22% (baseline: <1%)
- Latency increase: p99 went from 391ms to 3911ms


### Affected Services
- user-service
- billing-api
- payment-gateway

### Customer Impact

- 4292 customer-facing errors
- 79 support tickets created
- Estimated revenue impact: $2528


## Resolution


1. Increased connection pool size from 61 to 314
2. Reduced connection timeout from 106s to 29s  
3. Implemented connection pooling best practices
4. Added circuit breaker pattern for MongoDB calls


## Lessons Learned

### What Went Well

- Alert fired within 3 minutes of incident start
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
| P1 | Implement monitoring for deadlock in transaction | Database Team | 2025-09-03 |
| P2 | Update runbook | Infrastructure | 2025-09-10 |
| P2 | Add load test scenario | Backend Team | 2025-09-17 |
| P3 | Review similar services | Platform Engineering | 2025-09-26 |


## Related Incidents


- [[2025-08-27-previous-incident|Previous database incident]]
- [[runbook-user-service|user-service Runbook]]
- [[architecture-database|Database Architecture]]


---
*RCA prepared by Backend Team on 2025-08-30*
