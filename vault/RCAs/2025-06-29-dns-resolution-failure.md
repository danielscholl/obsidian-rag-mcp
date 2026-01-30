---
title: "2025-06-29 - DNS Resolution Failure in user-service"
date: 2025-06-29
severity: P1
services: [user-service, billing-api, search-api]
tags: [rca, p1, network]
status: resolved
duration_minutes: 129
author: Backend Team
---

# 2025-06-29 - DNS Resolution Failure in user-service

## Summary

On 2025-06-29, the user-service service experienced a dns resolution failure. The incident lasted approximately 129 minutes and affected 5595 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 02:45 | Monitoring alert triggered |
| 02:47 | On-call engineer paged |
| 02:50 | Initial investigation started |
| 02:55 | Root cause identified |
| 04:02 | Mitigation applied |
| 04:28 | Service recovery observed |
| 04:54 | Incident resolved |

## Root Cause


The incident was caused by dns resolution failure in the user-service service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 100% of requests affected
- Error rate spike: 10% (baseline: <1%)
- Latency increase: p99 went from 278ms to 2737ms


### Affected Services
- user-service
- billing-api
- search-api

### Customer Impact

- 601 customer-facing errors
- 22 support tickets created
- Estimated revenue impact: $19600


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 4 minutes of incident start
- On-call response was quick (7 minutes)
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
| P1 | Implement monitoring for dns resolution failure | DevOps | 2025-07-06 |
| P2 | Update runbook | Infrastructure | 2025-07-13 |
| P2 | Add load test scenario | Platform Engineering | 2025-07-20 |
| P3 | Review similar services | Platform Engineering | 2025-07-29 |


## Related Incidents


- [[2025-06-29-previous-incident|Previous network incident]]
- [[runbook-user-service|user-service Runbook]]
- [[architecture-network|Network Architecture]]


---
*RCA prepared by Backend Team on 2025-06-30*
