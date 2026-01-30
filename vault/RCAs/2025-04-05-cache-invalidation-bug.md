---
title: "2025-04-05 - Cache Invalidation Bug in order-service"
date: 2025-04-05
severity: P3
services: [order-service, auth-service, notification-service, analytics-pipeline]
tags: [rca, p3, application]
status: resolved
duration_minutes: 139
author: Backend Team
---

# 2025-04-05 - Cache Invalidation Bug in order-service

## Summary

On 2025-04-05, the order-service service experienced a cache invalidation bug. The incident lasted approximately 139 minutes and affected 3808 users and 4 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 15:28 | Monitoring alert triggered |
| 15:30 | On-call engineer paged |
| 15:33 | Initial investigation started |
| 15:38 | Root cause identified |
| 16:51 | Mitigation applied |
| 17:19 | Service recovery observed |
| 17:47 | Incident resolved |

## Root Cause


The incident was caused by cache invalidation bug in the order-service service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 81% of requests affected
- Error rate spike: 48% (baseline: <1%)
- Latency increase: p99 went from 475ms to 2549ms


### Affected Services
- order-service
- auth-service
- notification-service
- analytics-pipeline

### Customer Impact

- 2481 customer-facing errors
- 49 support tickets created
- Estimated revenue impact: $17556


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 2 minutes of incident start
- On-call response was quick (3 minutes)
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
| P1 | Implement monitoring for cache invalidation bug | Infrastructure | 2025-04-12 |
| P2 | Update runbook | Infrastructure | 2025-04-19 |
| P2 | Add load test scenario | Platform Engineering | 2025-04-26 |
| P3 | Review similar services | Infrastructure | 2025-05-05 |


## Related Incidents


- [[2025-04-05-previous-incident|Previous application incident]]
- [[runbook-order-service|order-service Runbook]]
- [[architecture-application|Application Architecture]]


---
*RCA prepared by Backend Team on 2025-04-06*
