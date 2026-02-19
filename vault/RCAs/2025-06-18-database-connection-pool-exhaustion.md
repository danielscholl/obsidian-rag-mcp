---
title: "2025-06-18 - Database Connection Pool Exhaustion in auth-service"
date: 2025-06-18
severity: P1
services: [auth-service, billing-api]
tags: [rca, p1, database]
status: resolved
duration_minutes: 149
author: Infrastructure
---

# 2025-06-18 - Database Connection Pool Exhaustion in auth-service

## Summary

On 2025-06-18, the auth-service service experienced a database connection pool exhaustion in PostgreSQL. The incident lasted approximately 149 minutes and affected 6225 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 08:41 | Monitoring alert triggered |
| 08:43 | On-call engineer paged |
| 08:46 | Initial investigation started |
| 08:51 | Root cause identified |
| 10:10 | Mitigation applied |
| 10:40 | Service recovery observed |
| 11:10 | Incident resolved |

## Root Cause


The root cause was traced to PostgreSQL connection handling. Under increased load from a marketing campaign, the connection pool (156 connections) became exhausted.

Key factors:
1. Connection timeout was set to 97 seconds, too long for our use case
2. No connection pool monitoring was in place
3. The service was holding connections during long-running operations

Technical details:
```
Error: PostgreSQLException: Connection pool exhausted
Max pool size: 166
Active connections: 422
Waiting requests: 819
```


## Impact


- Service degradation: 89% of requests affected
- Error rate spike: 12% (baseline: <1%)
- Latency increase: p99 went from 268ms to 4705ms


### Affected Services
- auth-service
- billing-api

### Customer Impact

- 1550 customer-facing errors
- 10 support tickets created
- Estimated revenue impact: $38344


## Resolution


1. Increased connection pool size from 100 to 325
2. Reduced connection timeout from 60s to 16s  
3. Implemented connection pooling best practices
4. Added circuit breaker pattern for PostgreSQL calls


## Lessons Learned

### What Went Well

- Alert fired within 5 minutes of incident start
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
| P1 | Implement monitoring for database connection pool exhaustion | SRE | 2025-06-25 |
| P2 | Update runbook | DevOps | 2025-07-02 |
| P2 | Add load test scenario | SRE | 2025-07-09 |
| P3 | Review similar services | Platform Engineering | 2025-07-18 |


## Related Incidents


- [[2025-06-18-previous-incident|Previous database incident]]
- [[runbook-auth-service|auth-service Runbook]]
- [[architecture-database|Database Architecture]]


---
*RCA prepared by Infrastructure on 2025-06-19*
