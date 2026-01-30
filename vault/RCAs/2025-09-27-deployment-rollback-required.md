---
title: "2025-09-27 - Deployment Rollback Required in notification-service"
date: 2025-09-27
severity: P2
services: [notification-service, billing-api, recommendation-engine]
tags: [rca, p2, deployment]
status: resolved
duration_minutes: 153
author: DevOps
---

# 2025-09-27 - Deployment Rollback Required in notification-service

## Summary

On 2025-09-27, the notification-service service experienced a deployment rollback required. The incident lasted approximately 153 minutes and affected 3800 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 10:26 | Monitoring alert triggered |
| 10:28 | On-call engineer paged |
| 10:31 | Initial investigation started |
| 10:36 | Root cause identified |
| 11:57 | Mitigation applied |
| 12:28 | Service recovery observed |
| 12:59 | Incident resolved |

## Root Cause


The incident was caused by deployment rollback required in the notification-service service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 70% of requests affected
- Error rate spike: 47% (baseline: <1%)
- Latency increase: p99 went from 321ms to 9586ms


### Affected Services
- notification-service
- billing-api
- recommendation-engine

### Customer Impact

- 3268 customer-facing errors
- 85 support tickets created
- Estimated revenue impact: $10457


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 3 minutes of incident start
- On-call response was quick (6 minutes)
- Cross-team collaboration was effective
- Communication to stakeholders was timely


### What Could Be Improved  

- Need better runbooks for deployment issues
- Monitoring coverage gaps identified
- Load testing should cover this scenario
- Need automated rollback for faster recovery


## Action Items


| Priority | Action | Owner | Due Date |
|----------|--------|-------|----------|
| P1 | Implement monitoring for deployment rollback required | DevOps | 2025-10-04 |
| P2 | Update runbook | Database Team | 2025-10-11 |
| P2 | Add load test scenario | DevOps | 2025-10-18 |
| P3 | Review similar services | Backend Team | 2025-10-27 |


## Related Incidents


- [[2025-09-27-previous-incident|Previous deployment incident]]
- [[runbook-notification-service|notification-service Runbook]]
- [[architecture-deployment|Deployment Architecture]]


---
*RCA prepared by DevOps on 2025-10-02*
