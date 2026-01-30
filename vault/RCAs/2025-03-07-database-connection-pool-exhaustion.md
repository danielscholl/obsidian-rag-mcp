---
title: "2025-03-07 - Database Connection Pool Exhaustion in order-service"
date: 2025-03-07
severity: P1
services: [order-service]
tags: [rca, p1, database]
status: resolved
duration_minutes: 162
author: Database Team
---

# 2025-03-07 - Database Connection Pool Exhaustion in order-service

## Summary

On 2025-03-07, the order-service service experienced a database connection pool exhaustion in Elasticsearch. The incident lasted approximately 162 minutes and affected 2351 users and 1 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 13:02 | Monitoring alert triggered |
| 13:04 | On-call engineer paged |
| 13:07 | Initial investigation started |
| 13:12 | Root cause identified |
| 14:39 | Mitigation applied |
| 15:11 | Service recovery observed |
| 15:44 | Incident resolved |

## Root Cause


The root cause was traced to Elasticsearch connection handling. Under increased load from a marketing campaign, the connection pool (86 connections) became exhausted.

Key factors:
1. Connection timeout was set to 61 seconds, too long for our use case
2. No connection pool monitoring was in place
3. The service was holding connections during long-running operations

Technical details:
```
Error: ElasticsearchException: Connection pool exhausted
Max pool size: 187
Active connections: 237
Waiting requests: 677
```


## Impact


- Service degradation: 50% of requests affected
- Error rate spike: 39% (baseline: <1%)
- Latency increase: p99 went from 137ms to 7957ms


### Affected Services
- order-service

### Customer Impact

- 3712 customer-facing errors
- 91 support tickets created
- Estimated revenue impact: $39613


## Resolution


1. Increased connection pool size from 61 to 433
2. Reduced connection timeout from 109s to 18s  
3. Implemented connection pooling best practices
4. Added circuit breaker pattern for Elasticsearch calls


## Lessons Learned

### What Went Well

- Alert fired within 1 minutes of incident start
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
| P1 | Implement monitoring for database connection pool exhaustion | Platform Engineering | 2025-03-14 |
| P2 | Update runbook | Infrastructure | 2025-03-21 |
| P2 | Add load test scenario | Database Team | 2025-03-28 |
| P3 | Review similar services | DevOps | 2025-04-06 |


## Related Incidents


- [[2025-03-07-previous-incident|Previous database incident]]
- [[runbook-order-service|order-service Runbook]]
- [[architecture-database|Database Architecture]]


---
*RCA prepared by Database Team on 2025-03-10*
