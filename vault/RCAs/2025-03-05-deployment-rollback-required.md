---
title: "2025-03-05 - Deployment Rollback Required in billing-api"
date: 2025-03-05
severity: P2
services: [billing-api, search-api]
tags: [rca, p2, deployment]
status: resolved
duration_minutes: 48
author: SRE
---

# 2025-03-05 - Deployment Rollback Required in billing-api

## Summary

On 2025-03-05, the billing-api service experienced a deployment rollback required. The incident lasted approximately 48 minutes and affected 668 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 10:08 | Monitoring alert triggered |
| 10:10 | On-call engineer paged |
| 10:13 | Initial investigation started |
| 10:18 | Root cause identified |
| 10:36 | Mitigation applied |
| 10:46 | Service recovery observed |
| 10:56 | Incident resolved |

## Root Cause


The incident was caused by deployment rollback required in the billing-api service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 100% of requests affected
- Error rate spike: 40% (baseline: <1%)
- Latency increase: p99 went from 129ms to 7435ms


### Affected Services
- billing-api
- search-api

### Customer Impact

- 157 customer-facing errors
- 45 support tickets created
- Estimated revenue impact: $46115


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 1 minutes of incident start
- On-call response was quick (9 minutes)
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
| P1 | Implement monitoring for deployment rollback required | Platform Engineering | 2025-03-12 |
| P2 | Update runbook | Backend Team | 2025-03-19 |
| P2 | Add load test scenario | Infrastructure | 2025-03-26 |
| P3 | Review similar services | Platform Engineering | 2025-04-04 |


## Related Incidents


- [[2025-03-05-previous-incident|Previous deployment incident]]
- [[runbook-billing-api|billing-api Runbook]]
- [[architecture-deployment|Deployment Architecture]]


---
*RCA prepared by SRE on 2025-03-09*
