---
title: "2025-04-13 - Memory Leak in Service in auth-service"
date: 2025-04-13
severity: P2
services: [notification-service, payment-gateway, auth-service]
tags: [rca, p2, application]
status: resolved
duration_minutes: 113
author: Database Team
---

# 2025-04-13 - Memory Leak in Service in auth-service

## Summary

On 2025-04-13, the auth-service service experienced a memory leak in service. The incident lasted approximately 113 minutes and affected 4204 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 22:27 | Monitoring alert triggered |
| 22:29 | On-call engineer paged |
| 22:32 | Initial investigation started |
| 22:37 | Root cause identified |
| 23:34 | Mitigation applied |
| 23:57 | Service recovery observed |
| 00:20 | Incident resolved |

## Root Cause


The incident was caused by memory leak in service in the auth-service service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 93% of requests affected
- Error rate spike: 17% (baseline: <1%)
- Latency increase: p99 went from 107ms to 4679ms


### Affected Services
- notification-service
- payment-gateway
- auth-service

### Customer Impact

- 1137 customer-facing errors
- 37 support tickets created
- Estimated revenue impact: $36771


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 1 minutes of incident start
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
| P1 | Implement monitoring for memory leak in service | Infrastructure | 2025-04-20 |
| P2 | Update runbook | SRE | 2025-04-27 |
| P2 | Add load test scenario | Infrastructure | 2025-05-04 |
| P3 | Review similar services | Platform Engineering | 2025-05-13 |


## Related Incidents


- [[2025-04-13-previous-incident|Previous application incident]]
- [[runbook-auth-service|auth-service Runbook]]
- [[architecture-application|Application Architecture]]


---
*RCA prepared by Database Team on 2025-04-15*
