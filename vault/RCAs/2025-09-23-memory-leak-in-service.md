---
title: "2025-09-23 - Memory Leak in Service in auth-service"
date: 2025-09-23
severity: P2
services: [auth-service]
tags: [rca, p2, application]
status: resolved
duration_minutes: 107
author: DevOps
---

# 2025-09-23 - Memory Leak in Service in auth-service

## Summary

On 2025-09-23, the auth-service service experienced a memory leak in service. The incident lasted approximately 107 minutes and affected 4429 users and 1 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 21:44 | Monitoring alert triggered |
| 21:46 | On-call engineer paged |
| 21:49 | Initial investigation started |
| 21:54 | Root cause identified |
| 22:48 | Mitigation applied |
| 23:09 | Service recovery observed |
| 23:31 | Incident resolved |

## Root Cause


The incident was caused by memory leak in service in the auth-service service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 59% of requests affected
- Error rate spike: 36% (baseline: <1%)
- Latency increase: p99 went from 453ms to 7157ms


### Affected Services
- auth-service

### Customer Impact

- 3128 customer-facing errors
- 41 support tickets created
- Estimated revenue impact: $27856


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 4 minutes of incident start
- On-call response was quick (8 minutes)
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
| P1 | Implement monitoring for memory leak in service | DevOps | 2025-09-30 |
| P2 | Update runbook | DevOps | 2025-10-07 |
| P2 | Add load test scenario | Backend Team | 2025-10-14 |
| P3 | Review similar services | Backend Team | 2025-10-23 |


## Related Incidents


- [[2025-09-23-previous-incident|Previous application incident]]
- [[runbook-auth-service|auth-service Runbook]]
- [[architecture-application|Application Architecture]]


---
*RCA prepared by DevOps on 2025-09-28*
