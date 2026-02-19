---
title: "2025-11-24 - Database Connection Pool Exhaustion in analytics-pipeline"
date: 2025-11-24
severity: P1
services: [analytics-pipeline, order-service]
tags: [rca, p1, database]
status: resolved
duration_minutes: 39
author: SRE
---

# 2025-11-24 - Database Connection Pool Exhaustion in analytics-pipeline

## Summary

On 2025-11-24, the analytics-pipeline service experienced a database connection pool exhaustion in Redis. The incident lasted approximately 39 minutes and affected 3566 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 01:43 | Monitoring alert triggered |
| 01:45 | On-call engineer paged |
| 01:48 | Initial investigation started |
| 01:53 | Root cause identified |
| 02:06 | Mitigation applied |
| 02:14 | Service recovery observed |
| 02:22 | Incident resolved |

## Root Cause


The root cause was traced to Redis connection handling. Under increased load from a marketing campaign, the connection pool (74 connections) became exhausted.

Key factors:
1. Connection timeout was set to 84 seconds, too long for our use case
2. No connection pool monitoring was in place
3. The service was holding connections during long-running operations

Technical details:
```
Error: RedisException: Connection pool exhausted
Max pool size: 130
Active connections: 348
Waiting requests: 887
```


## Impact


- Service degradation: 76% of requests affected
- Error rate spike: 12% (baseline: <1%)
- Latency increase: p99 went from 190ms to 2421ms


### Affected Services
- analytics-pipeline
- order-service

### Customer Impact

- 4443 customer-facing errors
- 29 support tickets created
- Estimated revenue impact: $33196


## Resolution


1. Increased connection pool size from 67 to 307
2. Reduced connection timeout from 76s to 30s  
3. Implemented connection pooling best practices
4. Added circuit breaker pattern for Redis calls


## Lessons Learned

### What Went Well

- Alert fired within 5 minutes of incident start
- On-call response was quick (4 minutes)
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
| P1 | Implement monitoring for database connection pool exhaustion | Database Team | 2025-12-01 |
| P2 | Update runbook | Platform Engineering | 2025-12-08 |
| P2 | Add load test scenario | Platform Engineering | 2025-12-15 |
| P3 | Review similar services | Backend Team | 2025-12-24 |


## Related Incidents


- [[2025-11-24-previous-incident|Previous database incident]]
- [[runbook-analytics-pipeline|analytics-pipeline Runbook]]
- [[architecture-database|Database Architecture]]


---
*RCA prepared by SRE on 2025-11-27*
