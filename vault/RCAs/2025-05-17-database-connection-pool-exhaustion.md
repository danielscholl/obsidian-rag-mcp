---
title: "2025-05-17 - Database Connection Pool Exhaustion in payment-gateway"
date: 2025-05-17
severity: P1
services: [payment-gateway, search-api, user-service]
tags: [rca, p1, database]
status: resolved
duration_minutes: 158
author: Database Team
---

# 2025-05-17 - Database Connection Pool Exhaustion in payment-gateway

## Summary

On 2025-05-17, the payment-gateway service experienced a database connection pool exhaustion in Elasticsearch. The incident lasted approximately 158 minutes and affected 2884 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 03:42 | Monitoring alert triggered |
| 03:44 | On-call engineer paged |
| 03:47 | Initial investigation started |
| 03:52 | Root cause identified |
| 05:16 | Mitigation applied |
| 05:48 | Service recovery observed |
| 06:20 | Incident resolved |

## Root Cause


The root cause was traced to Elasticsearch connection handling. Under increased load from a marketing campaign, the connection pool (133 connections) became exhausted.

Key factors:
1. Connection timeout was set to 47 seconds, too long for our use case
2. No connection pool monitoring was in place
3. The service was holding connections during long-running operations

Technical details:
```
Error: ElasticsearchException: Connection pool exhausted
Max pool size: 116
Active connections: 352
Waiting requests: 621
```


## Impact


- Service degradation: 67% of requests affected
- Error rate spike: 22% (baseline: <1%)
- Latency increase: p99 went from 461ms to 2499ms


### Affected Services
- payment-gateway
- search-api
- user-service

### Customer Impact

- 1957 customer-facing errors
- 74 support tickets created
- Estimated revenue impact: $43501


## Resolution


1. Increased connection pool size from 61 to 237
2. Reduced connection timeout from 70s to 11s  
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
| P1 | Implement monitoring for database connection pool exhaustion | SRE | 2025-05-24 |
| P2 | Update runbook | Infrastructure | 2025-05-31 |
| P2 | Add load test scenario | Platform Engineering | 2025-06-07 |
| P3 | Review similar services | Backend Team | 2025-06-16 |


## Related Incidents


- [[2025-05-17-previous-incident|Previous database incident]]
- [[runbook-payment-gateway|payment-gateway Runbook]]
- [[architecture-database|Database Architecture]]


---
*RCA prepared by Database Team on 2025-05-22*
