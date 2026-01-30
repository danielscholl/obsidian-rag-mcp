---
title: "2025-03-15 - Deadlock in Transaction in auth-service"
date: 2025-03-15
severity: P2
services: [payment-gateway, auth-service, recommendation-engine]
tags: [rca, p2, database]
status: resolved
duration_minutes: 15
author: Platform Engineering
---

# 2025-03-15 - Deadlock in Transaction in auth-service

## Summary

On 2025-03-15, the auth-service service experienced a deadlock in transaction in Redis. The incident lasted approximately 15 minutes and affected 3710 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 20:43 | Monitoring alert triggered |
| 20:45 | On-call engineer paged |
| 20:48 | Initial investigation started |
| 20:53 | Root cause identified |
| 20:52 | Mitigation applied |
| 20:55 | Service recovery observed |
| 20:58 | Incident resolved |

## Root Cause


The root cause was traced to Redis connection handling. Under increased load from a marketing campaign, the connection pool (151 connections) became exhausted.

Key factors:
1. Connection timeout was set to 43 seconds, too long for our use case
2. No connection pool monitoring was in place
3. The service was holding connections during long-running operations

Technical details:
```
Error: RedisException: Connection pool exhausted
Max pool size: 135
Active connections: 443
Waiting requests: 557
```


## Impact


- Service degradation: 77% of requests affected
- Error rate spike: 40% (baseline: <1%)
- Latency increase: p99 went from 410ms to 9158ms


### Affected Services
- payment-gateway
- auth-service
- recommendation-engine

### Customer Impact

- 1375 customer-facing errors
- 36 support tickets created
- Estimated revenue impact: $15599


## Resolution


1. Increased connection pool size from 51 to 272
2. Reduced connection timeout from 88s to 17s  
3. Implemented connection pooling best practices
4. Added circuit breaker pattern for Redis calls


## Lessons Learned

### What Went Well

- Alert fired within 5 minutes of incident start
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
| P1 | Implement monitoring for deadlock in transaction | Platform Engineering | 2025-03-22 |
| P2 | Update runbook | Infrastructure | 2025-03-29 |
| P2 | Add load test scenario | Backend Team | 2025-04-05 |
| P3 | Review similar services | DevOps | 2025-04-14 |


## Related Incidents


- [[2025-03-15-previous-incident|Previous database incident]]
- [[runbook-auth-service|auth-service Runbook]]
- [[architecture-database|Database Architecture]]


---
*RCA prepared by Platform Engineering on 2025-03-18*
