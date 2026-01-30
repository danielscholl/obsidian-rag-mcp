---
title: "2025-09-27 - Cache Invalidation Bug in user-service"
date: 2025-09-27
severity: P3
services: [user-service, recommendation-engine, analytics-pipeline, order-service]
tags: [rca, p3, application]
status: resolved
duration_minutes: 134
author: Backend Team
---

# 2025-09-27 - Cache Invalidation Bug in user-service

## Summary

On 2025-09-27, the user-service service experienced a cache invalidation bug. The incident lasted approximately 134 minutes and affected 6126 users and 4 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 19:03 | Monitoring alert triggered |
| 19:05 | On-call engineer paged |
| 19:08 | Initial investigation started |
| 19:13 | Root cause identified |
| 20:23 | Mitigation applied |
| 20:50 | Service recovery observed |
| 21:17 | Incident resolved |

## Root Cause


The incident was caused by cache invalidation bug in the user-service service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 59% of requests affected
- Error rate spike: 10% (baseline: <1%)
- Latency increase: p99 went from 161ms to 5012ms


### Affected Services
- user-service
- recommendation-engine
- analytics-pipeline
- order-service

### Customer Impact

- 1226 customer-facing errors
- 77 support tickets created
- Estimated revenue impact: $44674


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 3 minutes of incident start
- On-call response was quick (5 minutes)
- Cross-team collaboration was effective
- Communication to stakeholders was timely


### What Could Be Improved  

- Need better runbooks for application issues
- Monitoring coverage gaps identified
- Load testing should cover this scenario
- Need automated rollback for faster recovery


## Action Items


| Priority | Action | Owner | Due Date |
|----------|--------|-------|----------|
| P1 | Implement monitoring for cache invalidation bug | Infrastructure | 2025-10-04 |
| P2 | Update runbook | Database Team | 2025-10-11 |
| P2 | Add load test scenario | SRE | 2025-10-18 |
| P3 | Review similar services | Backend Team | 2025-10-27 |


## Related Incidents


- [[2025-09-27-previous-incident|Previous application incident]]
- [[runbook-user-service|user-service Runbook]]
- [[architecture-application|Application Architecture]]


---
*RCA prepared by Backend Team on 2025-09-30*
