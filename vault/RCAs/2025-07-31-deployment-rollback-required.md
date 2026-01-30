---
title: "2025-07-31 - Deployment Rollback Required in auth-service"
date: 2025-07-31
severity: P2
services: [auth-service, inventory-api]
tags: [rca, p2, deployment]
status: resolved
duration_minutes: 22
author: Database Team
---

# 2025-07-31 - Deployment Rollback Required in auth-service

## Summary

On 2025-07-31, the auth-service service experienced a deployment rollback required. The incident lasted approximately 22 minutes and affected 3977 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 12:17 | Monitoring alert triggered |
| 12:19 | On-call engineer paged |
| 12:22 | Initial investigation started |
| 12:27 | Root cause identified |
| 12:30 | Mitigation applied |
| 12:34 | Service recovery observed |
| 12:39 | Incident resolved |

## Root Cause


The incident was caused by deployment rollback required in the auth-service service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 71% of requests affected
- Error rate spike: 48% (baseline: <1%)
- Latency increase: p99 went from 140ms to 6720ms


### Affected Services
- auth-service
- inventory-api

### Customer Impact

- 2324 customer-facing errors
- 98 support tickets created
- Estimated revenue impact: $43618


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 2 minutes of incident start
- On-call response was quick (10 minutes)
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
| P1 | Implement monitoring for deployment rollback required | SRE | 2025-08-07 |
| P2 | Update runbook | Platform Engineering | 2025-08-14 |
| P2 | Add load test scenario | Infrastructure | 2025-08-21 |
| P3 | Review similar services | Infrastructure | 2025-08-30 |


## Related Incidents


- [[2025-07-31-previous-incident|Previous deployment incident]]
- [[runbook-auth-service|auth-service Runbook]]
- [[architecture-deployment|Deployment Architecture]]


---
*RCA prepared by Database Team on 2025-08-03*
