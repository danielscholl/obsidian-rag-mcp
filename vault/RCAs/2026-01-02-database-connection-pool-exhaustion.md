---
title: "2026-01-02 - Database Connection Pool Exhaustion in billing-api"
date: 2026-01-02
severity: P1
services: [billing-api, analytics-pipeline]
tags: [rca, p1, database]
status: resolved
duration_minutes: 56
author: SRE
---

# 2026-01-02 - Database Connection Pool Exhaustion in billing-api

## Summary

On 2026-01-02, the billing-api service experienced a database connection pool exhaustion in Elasticsearch. The incident lasted approximately 56 minutes and affected 3661 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 05:02 | Monitoring alert triggered |
| 05:04 | On-call engineer paged |
| 05:07 | Initial investigation started |
| 05:12 | Root cause identified |
| 05:35 | Mitigation applied |
| 05:46 | Service recovery observed |
| 05:58 | Incident resolved |

## Root Cause


The root cause was traced to Elasticsearch connection handling. Under increased load from a marketing campaign, the connection pool (102 connections) became exhausted.

Key factors:
1. Connection timeout was set to 104 seconds, too long for our use case
2. No connection pool monitoring was in place
3. The service was holding connections during long-running operations

Technical details:
```
Error: ElasticsearchException: Connection pool exhausted
Max pool size: 161
Active connections: 265
Waiting requests: 561
```


## Impact


- Service degradation: 53% of requests affected
- Error rate spike: 16% (baseline: <1%)
- Latency increase: p99 went from 284ms to 5911ms


### Affected Services
- billing-api
- analytics-pipeline

### Customer Impact

- 4298 customer-facing errors
- 98 support tickets created
- Estimated revenue impact: $40164


## Resolution


1. Increased connection pool size from 51 to 455
2. Reduced connection timeout from 93s to 13s  
3. Implemented connection pooling best practices
4. Added circuit breaker pattern for Elasticsearch calls


## Lessons Learned

### What Went Well

- Alert fired within 3 minutes of incident start
- On-call response was quick (8 minutes)
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
| P1 | Implement monitoring for database connection pool exhaustion | Infrastructure | 2026-01-09 |
| P2 | Update runbook | SRE | 2026-01-16 |
| P2 | Add load test scenario | DevOps | 2026-01-23 |
| P3 | Review similar services | SRE | 2026-02-01 |


## Related Incidents


- [[2026-01-02-previous-incident|Previous database incident]]
- [[runbook-billing-api|billing-api Runbook]]
- [[architecture-database|Database Architecture]]


---
*RCA prepared by SRE on 2026-01-07*
