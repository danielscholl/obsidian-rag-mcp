---
title: "2025-05-11 - Database Connection Pool Exhaustion in order-service"
date: 2025-05-11
severity: P1
services: [order-service, billing-api, analytics-pipeline, search-api]
tags: [rca, p1, database]
status: resolved
duration_minutes: 130
author: DevOps
---

# 2025-05-11 - Database Connection Pool Exhaustion in order-service

## Summary

On 2025-05-11, the order-service service experienced a database connection pool exhaustion in MongoDB. The incident lasted approximately 130 minutes and affected 1843 users and 4 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 04:30 | Monitoring alert triggered |
| 04:32 | On-call engineer paged |
| 04:35 | Initial investigation started |
| 04:40 | Root cause identified |
| 05:48 | Mitigation applied |
| 06:14 | Service recovery observed |
| 06:40 | Incident resolved |

## Root Cause


The root cause was traced to MongoDB connection handling. Under increased load from a marketing campaign, the connection pool (107 connections) became exhausted.

Key factors:
1. Connection timeout was set to 51 seconds, too long for our use case
2. No connection pool monitoring was in place
3. The service was holding connections during long-running operations

Technical details:
```
Error: MongoDBException: Connection pool exhausted
Max pool size: 95
Active connections: 251
Waiting requests: 807
```


## Impact


- Service degradation: 67% of requests affected
- Error rate spike: 14% (baseline: <1%)
- Latency increase: p99 went from 195ms to 6576ms


### Affected Services
- order-service
- billing-api
- analytics-pipeline
- search-api

### Customer Impact

- 1618 customer-facing errors
- 52 support tickets created
- Estimated revenue impact: $31523


## Resolution


1. Increased connection pool size from 57 to 437
2. Reduced connection timeout from 101s to 24s  
3. Implemented connection pooling best practices
4. Added circuit breaker pattern for MongoDB calls


## Lessons Learned

### What Went Well

- Alert fired within 4 minutes of incident start
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
| P1 | Implement monitoring for database connection pool exhaustion | Database Team | 2025-05-18 |
| P2 | Update runbook | Database Team | 2025-05-25 |
| P2 | Add load test scenario | Infrastructure | 2025-06-01 |
| P3 | Review similar services | Infrastructure | 2025-06-10 |


## Related Incidents


- [[2025-05-11-previous-incident|Previous database incident]]
- [[runbook-order-service|order-service Runbook]]
- [[architecture-database|Database Architecture]]


---
*RCA prepared by DevOps on 2025-05-15*
