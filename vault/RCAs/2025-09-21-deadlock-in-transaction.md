---
title: "2025-09-21 - Deadlock in Transaction in billing-api"
date: 2025-09-21
severity: P2
services: [billing-api, user-service]
tags: [rca, p2, database]
status: resolved
duration_minutes: 146
author: Backend Team
---

# 2025-09-21 - Deadlock in Transaction in billing-api

## Summary

On 2025-09-21, the billing-api service experienced a deadlock in transaction in Elasticsearch. The incident lasted approximately 146 minutes and affected 9936 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 02:53 | Monitoring alert triggered |
| 02:55 | On-call engineer paged |
| 02:58 | Initial investigation started |
| 03:03 | Root cause identified |
| 04:20 | Mitigation applied |
| 04:49 | Service recovery observed |
| 05:19 | Incident resolved |

## Root Cause


The root cause was traced to Elasticsearch connection handling. Under increased load from a marketing campaign, the connection pool (151 connections) became exhausted.

Key factors:
1. Connection timeout was set to 80 seconds, too long for our use case
2. No connection pool monitoring was in place
3. The service was holding connections during long-running operations

Technical details:
```
Error: ElasticsearchException: Connection pool exhausted
Max pool size: 72
Active connections: 286
Waiting requests: 667
```


## Impact


- Service degradation: 63% of requests affected
- Error rate spike: 40% (baseline: <1%)
- Latency increase: p99 went from 114ms to 3205ms


### Affected Services
- billing-api
- user-service

### Customer Impact

- 719 customer-facing errors
- 10 support tickets created
- Estimated revenue impact: $16056


## Resolution


1. Increased connection pool size from 72 to 322
2. Reduced connection timeout from 99s to 18s  
3. Implemented connection pooling best practices
4. Added circuit breaker pattern for Elasticsearch calls


## Lessons Learned

### What Went Well

- Alert fired within 3 minutes of incident start
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
| P1 | Implement monitoring for deadlock in transaction | DevOps | 2025-09-28 |
| P2 | Update runbook | Database Team | 2025-10-05 |
| P2 | Add load test scenario | Platform Engineering | 2025-10-12 |
| P3 | Review similar services | Infrastructure | 2025-10-21 |


## Related Incidents


- [[2025-09-21-previous-incident|Previous database incident]]
- [[runbook-billing-api|billing-api Runbook]]
- [[architecture-database|Database Architecture]]


---
*RCA prepared by Backend Team on 2025-09-22*
