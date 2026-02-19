---
title: "2025-04-29 - Third-Party API Degradation in notification-service"
date: 2025-04-29
severity: P2
services: [notification-service, search-api, payment-gateway, user-service]
tags: [rca, p2, external]
status: resolved
duration_minutes: 63
author: Backend Team
---

# 2025-04-29 - Third-Party API Degradation in notification-service

## Summary

On 2025-04-29, the notification-service service experienced a third-party api degradation. The incident lasted approximately 63 minutes and affected 8921 users and 4 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 09:00 | Monitoring alert triggered |
| 09:02 | On-call engineer paged |
| 09:05 | Initial investigation started |
| 09:10 | Root cause identified |
| 09:37 | Mitigation applied |
| 09:50 | Service recovery observed |
| 10:03 | Incident resolved |

## Root Cause


The incident was caused by third-party api degradation in the notification-service service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 74% of requests affected
- Error rate spike: 39% (baseline: <1%)
- Latency increase: p99 went from 218ms to 7053ms


### Affected Services
- notification-service
- search-api
- payment-gateway
- user-service

### Customer Impact

- 679 customer-facing errors
- 39 support tickets created
- Estimated revenue impact: $12749


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 5 minutes of incident start
- On-call response was quick (8 minutes)
- Cross-team collaboration was effective
- Communication to stakeholders was timely


### What Could Be Improved  

- Need better runbooks for external issues
- Monitoring coverage gaps identified
- Load testing should cover this scenario
- Need automated rollback for faster recovery


## Action Items


| Priority | Action | Owner | Due Date |
|----------|--------|-------|----------|
| P1 | Implement monitoring for third-party api degradation | SRE | 2025-05-06 |
| P2 | Update runbook | DevOps | 2025-05-13 |
| P2 | Add load test scenario | Database Team | 2025-05-20 |
| P3 | Review similar services | DevOps | 2025-05-29 |


## Related Incidents


- [[2025-04-29-previous-incident|Previous external incident]]
- [[runbook-notification-service|notification-service Runbook]]
- [[architecture-external|External Architecture]]


---
*RCA prepared by Backend Team on 2025-05-04*
