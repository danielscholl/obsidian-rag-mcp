---
title: "2025-01-29 - DNS Resolution Failure in user-service"
date: 2025-01-29
severity: P1
services: [billing-api, user-service, analytics-pipeline]
tags: [rca, p1, network]
status: resolved
duration_minutes: 166
author: Database Team
---

# 2025-01-29 - DNS Resolution Failure in user-service

## Summary

On 2025-01-29, the user-service service experienced a dns resolution failure. The incident lasted approximately 166 minutes and affected 9886 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 15:53 | Monitoring alert triggered |
| 15:55 | On-call engineer paged |
| 15:58 | Initial investigation started |
| 16:03 | Root cause identified |
| 17:32 | Mitigation applied |
| 18:05 | Service recovery observed |
| 18:39 | Incident resolved |

## Root Cause


The incident was caused by dns resolution failure in the user-service service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 65% of requests affected
- Error rate spike: 33% (baseline: <1%)
- Latency increase: p99 went from 391ms to 5878ms


### Affected Services
- billing-api
- user-service
- analytics-pipeline

### Customer Impact

- 4516 customer-facing errors
- 81 support tickets created
- Estimated revenue impact: $4108


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

- Need better runbooks for network issues
- Monitoring coverage gaps identified
- Load testing should cover this scenario
- Need automated rollback for faster recovery


## Action Items


| Priority | Action | Owner | Due Date |
|----------|--------|-------|----------|
| P1 | Implement monitoring for dns resolution failure | DevOps | 2025-02-05 |
| P2 | Update runbook | Backend Team | 2025-02-12 |
| P2 | Add load test scenario | Infrastructure | 2025-02-19 |
| P3 | Review similar services | DevOps | 2025-02-28 |


## Related Incidents


- [[2025-01-29-previous-incident|Previous network incident]]
- [[runbook-user-service|user-service Runbook]]
- [[architecture-network|Network Architecture]]


---
*RCA prepared by Database Team on 2025-02-01*
