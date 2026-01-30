---
title: "2025-05-08 - DNS Resolution Failure in notification-service"
date: 2025-05-08
severity: P1
services: [notification-service, search-api]
tags: [rca, p1, network]
status: resolved
duration_minutes: 167
author: SRE
---

# 2025-05-08 - DNS Resolution Failure in notification-service

## Summary

On 2025-05-08, the notification-service service experienced a dns resolution failure. The incident lasted approximately 167 minutes and affected 2428 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 07:50 | Monitoring alert triggered |
| 07:52 | On-call engineer paged |
| 07:55 | Initial investigation started |
| 08:00 | Root cause identified |
| 09:30 | Mitigation applied |
| 10:03 | Service recovery observed |
| 10:37 | Incident resolved |

## Root Cause


The incident was caused by dns resolution failure in the notification-service service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 60% of requests affected
- Error rate spike: 21% (baseline: <1%)
- Latency increase: p99 went from 387ms to 5811ms


### Affected Services
- notification-service
- search-api

### Customer Impact

- 752 customer-facing errors
- 40 support tickets created
- Estimated revenue impact: $21585


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 5 minutes of incident start
- On-call response was quick (2 minutes)
- Cross-team collaboration was effective
- Communication to stakeholders was timely


### What Could Be Improved  

- Need better runbooks for network issues
- Monitoring coverage gaps identified
- Load testing should cover this scenario
- Need automated rollback for faster recovery


## Action Items


| Priority | Action | Owner | Due Date |
|----------|--------|-------|----------|
| P1 | Implement monitoring for dns resolution failure | Backend Team | 2025-05-15 |
| P2 | Update runbook | DevOps | 2025-05-22 |
| P2 | Add load test scenario | Database Team | 2025-05-29 |
| P3 | Review similar services | DevOps | 2025-06-07 |


## Related Incidents


- [[2025-05-08-previous-incident|Previous network incident]]
- [[runbook-notification-service|notification-service Runbook]]
- [[architecture-network|Network Architecture]]


---
*RCA prepared by SRE on 2025-05-10*
