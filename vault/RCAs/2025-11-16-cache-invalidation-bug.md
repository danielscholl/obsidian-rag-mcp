---
title: "2025-11-16 - Cache Invalidation Bug in notification-service"
date: 2025-11-16
severity: P3
services: [notification-service, auth-service]
tags: [rca, p3, application]
status: resolved
duration_minutes: 104
author: Platform Engineering
---

# 2025-11-16 - Cache Invalidation Bug in notification-service

## Summary

On 2025-11-16, the notification-service service experienced a cache invalidation bug. The incident lasted approximately 104 minutes and affected 5718 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 11:38 | Monitoring alert triggered |
| 11:40 | On-call engineer paged |
| 11:43 | Initial investigation started |
| 11:48 | Root cause identified |
| 12:40 | Mitigation applied |
| 13:01 | Service recovery observed |
| 13:22 | Incident resolved |

## Root Cause


The incident was caused by cache invalidation bug in the notification-service service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 99% of requests affected
- Error rate spike: 22% (baseline: <1%)
- Latency increase: p99 went from 471ms to 6173ms


### Affected Services
- notification-service
- auth-service

### Customer Impact

- 1137 customer-facing errors
- 40 support tickets created
- Estimated revenue impact: $24191


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 4 minutes of incident start
- On-call response was quick (9 minutes)
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
| P1 | Implement monitoring for cache invalidation bug | Infrastructure | 2025-11-23 |
| P2 | Update runbook | Backend Team | 2025-11-30 |
| P2 | Add load test scenario | SRE | 2025-12-07 |
| P3 | Review similar services | Infrastructure | 2025-12-16 |


## Related Incidents


- [[2025-11-16-previous-incident|Previous application incident]]
- [[runbook-notification-service|notification-service Runbook]]
- [[architecture-application|Application Architecture]]


---
*RCA prepared by Platform Engineering on 2025-11-17*
