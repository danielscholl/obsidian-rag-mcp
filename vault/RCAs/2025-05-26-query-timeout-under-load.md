---
title: "2025-05-26 - Query Timeout Under Load in billing-api"
date: 2025-05-26
severity: P2
services: [billing-api, payment-gateway]
tags: [rca, p2, database]
status: resolved
duration_minutes: 150
author: SRE
---

# 2025-05-26 - Query Timeout Under Load in billing-api

## Summary

On 2025-05-26, the billing-api service experienced a query timeout under load in MongoDB. The incident lasted approximately 150 minutes and affected 8061 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 06:10 | Monitoring alert triggered |
| 06:12 | On-call engineer paged |
| 06:15 | Initial investigation started |
| 06:20 | Root cause identified |
| 07:40 | Mitigation applied |
| 08:10 | Service recovery observed |
| 08:40 | Incident resolved |

## Root Cause


The root cause was traced to MongoDB connection handling. Under increased load from a marketing campaign, the connection pool (105 connections) became exhausted.

Key factors:
1. Connection timeout was set to 75 seconds, too long for our use case
2. No connection pool monitoring was in place
3. The service was holding connections during long-running operations

Technical details:
```
Error: MongoDBException: Connection pool exhausted
Max pool size: 51
Active connections: 213
Waiting requests: 392
```


## Impact


- Service degradation: 87% of requests affected
- Error rate spike: 41% (baseline: <1%)
- Latency increase: p99 went from 416ms to 8406ms


### Affected Services
- billing-api
- payment-gateway

### Customer Impact

- 4108 customer-facing errors
- 15 support tickets created
- Estimated revenue impact: $33126


## Resolution


1. Increased connection pool size from 73 to 438
2. Reduced connection timeout from 95s to 29s  
3. Implemented connection pooling best practices
4. Added circuit breaker pattern for MongoDB calls


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
| P1 | Implement monitoring for query timeout under load | Database Team | 2025-06-02 |
| P2 | Update runbook | Platform Engineering | 2025-06-09 |
| P2 | Add load test scenario | Database Team | 2025-06-16 |
| P3 | Review similar services | SRE | 2025-06-25 |


## Related Incidents


- [[2025-05-26-previous-incident|Previous database incident]]
- [[runbook-billing-api|billing-api Runbook]]
- [[architecture-database|Database Architecture]]


---
*RCA prepared by SRE on 2025-05-27*
