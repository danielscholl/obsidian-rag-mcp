---
title: "2025-11-06 - Query Timeout Under Load in inventory-api"
date: 2025-11-06
severity: P2
services: [inventory-api, notification-service]
tags: [rca, p2, database]
status: resolved
duration_minutes: 32
author: SRE
---

# 2025-11-06 - Query Timeout Under Load in inventory-api

## Summary

On 2025-11-06, the inventory-api service experienced a query timeout under load in Elasticsearch. The incident lasted approximately 32 minutes and affected 1863 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 01:06 | Monitoring alert triggered |
| 01:08 | On-call engineer paged |
| 01:11 | Initial investigation started |
| 01:16 | Root cause identified |
| 01:25 | Mitigation applied |
| 01:31 | Service recovery observed |
| 01:38 | Incident resolved |

## Root Cause


The root cause was traced to Elasticsearch connection handling. Under increased load from a marketing campaign, the connection pool (75 connections) became exhausted.

Key factors:
1. Connection timeout was set to 101 seconds, too long for our use case
2. No connection pool monitoring was in place
3. The service was holding connections during long-running operations

Technical details:
```
Error: ElasticsearchException: Connection pool exhausted
Max pool size: 64
Active connections: 330
Waiting requests: 747
```


## Impact


- Service degradation: 95% of requests affected
- Error rate spike: 33% (baseline: <1%)
- Latency increase: p99 went from 493ms to 8795ms


### Affected Services
- inventory-api
- notification-service

### Customer Impact

- 4482 customer-facing errors
- 40 support tickets created
- Estimated revenue impact: $5789


## Resolution


1. Increased connection pool size from 54 to 482
2. Reduced connection timeout from 62s to 27s  
3. Implemented connection pooling best practices
4. Added circuit breaker pattern for Elasticsearch calls


## Lessons Learned

### What Went Well

- Alert fired within 3 minutes of incident start
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
| P1 | Implement monitoring for query timeout under load | DevOps | 2025-11-13 |
| P2 | Update runbook | DevOps | 2025-11-20 |
| P2 | Add load test scenario | Backend Team | 2025-11-27 |
| P3 | Review similar services | Database Team | 2025-12-06 |


## Related Incidents


- [[2025-11-06-previous-incident|Previous database incident]]
- [[runbook-inventory-api|inventory-api Runbook]]
- [[architecture-database|Database Architecture]]


---
*RCA prepared by SRE on 2025-11-11*
