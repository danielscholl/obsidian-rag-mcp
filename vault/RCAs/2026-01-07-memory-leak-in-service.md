---
title: "2026-01-07 - Memory Leak in Service in notification-service"
date: 2026-01-07
severity: P2
services: [notification-service, payment-gateway, billing-api]
tags: [rca, p2, application]
status: resolved
duration_minutes: 112
author: Platform Engineering
---

# 2026-01-07 - Memory Leak in Service in notification-service

## Summary

On 2026-01-07, the notification-service service experienced a memory leak in service. The incident lasted approximately 112 minutes and affected 1745 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 10:05 | Monitoring alert triggered |
| 10:07 | On-call engineer paged |
| 10:10 | Initial investigation started |
| 10:15 | Root cause identified |
| 11:12 | Mitigation applied |
| 11:34 | Service recovery observed |
| 11:57 | Incident resolved |

## Root Cause


The incident was caused by memory leak in service in the notification-service service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 99% of requests affected
- Error rate spike: 17% (baseline: <1%)
- Latency increase: p99 went from 105ms to 9311ms


### Affected Services
- notification-service
- payment-gateway
- billing-api

### Customer Impact

- 1428 customer-facing errors
- 47 support tickets created
- Estimated revenue impact: $31817


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 4 minutes of incident start
- On-call response was quick (4 minutes)
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
| P1 | Implement monitoring for memory leak in service | DevOps | 2026-01-14 |
| P2 | Update runbook | Database Team | 2026-01-21 |
| P2 | Add load test scenario | DevOps | 2026-01-28 |
| P3 | Review similar services | DevOps | 2026-02-06 |


## Related Incidents


- [[2026-01-07-previous-incident|Previous application incident]]
- [[runbook-notification-service|notification-service Runbook]]
- [[architecture-application|Application Architecture]]


---
*RCA prepared by Platform Engineering on 2026-01-10*
