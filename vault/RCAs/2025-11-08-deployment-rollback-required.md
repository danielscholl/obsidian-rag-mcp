---
title: "2025-11-08 - Deployment Rollback Required in user-service"
date: 2025-11-08
severity: P2
services: [search-api, user-service]
tags: [rca, p2, deployment]
status: resolved
duration_minutes: 115
author: SRE
---

# 2025-11-08 - Deployment Rollback Required in user-service

## Summary

On 2025-11-08, the user-service service experienced a deployment rollback required. The incident lasted approximately 115 minutes and affected 3552 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 21:44 | Monitoring alert triggered |
| 21:46 | On-call engineer paged |
| 21:49 | Initial investigation started |
| 21:54 | Root cause identified |
| 22:53 | Mitigation applied |
| 23:16 | Service recovery observed |
| 23:39 | Incident resolved |

## Root Cause


The incident was caused by deployment rollback required in the user-service service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 84% of requests affected
- Error rate spike: 24% (baseline: <1%)
- Latency increase: p99 went from 213ms to 4163ms


### Affected Services
- search-api
- user-service

### Customer Impact

- 2944 customer-facing errors
- 70 support tickets created
- Estimated revenue impact: $45767


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 4 minutes of incident start
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
| P1 | Implement monitoring for deployment rollback required | SRE | 2025-11-15 |
| P2 | Update runbook | DevOps | 2025-11-22 |
| P2 | Add load test scenario | Platform Engineering | 2025-11-29 |
| P3 | Review similar services | Backend Team | 2025-12-08 |


## Related Incidents


- [[2025-11-08-previous-incident|Previous deployment incident]]
- [[runbook-user-service|user-service Runbook]]
- [[architecture-deployment|Deployment Architecture]]


---
*RCA prepared by SRE on 2025-11-09*
