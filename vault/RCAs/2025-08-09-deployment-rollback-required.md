---
title: "2025-08-09 - Deployment Rollback Required in notification-service"
date: 2025-08-09
severity: P2
services: [notification-service, payment-gateway]
tags: [rca, p2, deployment]
status: resolved
duration_minutes: 133
author: SRE
---

# 2025-08-09 - Deployment Rollback Required in notification-service

## Summary

On 2025-08-09, the notification-service service experienced a deployment rollback required. The incident lasted approximately 133 minutes and affected 5413 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 10:46 | Monitoring alert triggered |
| 10:48 | On-call engineer paged |
| 10:51 | Initial investigation started |
| 10:56 | Root cause identified |
| 12:05 | Mitigation applied |
| 12:32 | Service recovery observed |
| 12:59 | Incident resolved |

## Root Cause


The incident was caused by deployment rollback required in the notification-service service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 69% of requests affected
- Error rate spike: 50% (baseline: <1%)
- Latency increase: p99 went from 286ms to 9736ms


### Affected Services
- notification-service
- payment-gateway

### Customer Impact

- 3390 customer-facing errors
- 43 support tickets created
- Estimated revenue impact: $8616


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 5 minutes of incident start
- On-call response was quick (7 minutes)
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
| P1 | Implement monitoring for deployment rollback required | Infrastructure | 2025-08-16 |
| P2 | Update runbook | Database Team | 2025-08-23 |
| P2 | Add load test scenario | Database Team | 2025-08-30 |
| P3 | Review similar services | SRE | 2025-09-08 |


## Related Incidents


- [[2025-08-09-previous-incident|Previous deployment incident]]
- [[runbook-notification-service|notification-service Runbook]]
- [[architecture-deployment|Deployment Architecture]]


---
*RCA prepared by SRE on 2025-08-13*
