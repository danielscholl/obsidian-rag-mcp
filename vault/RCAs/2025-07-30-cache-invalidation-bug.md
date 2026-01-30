---
title: "2025-07-30 - Cache Invalidation Bug in recommendation-engine"
date: 2025-07-30
severity: P3
services: [recommendation-engine, billing-api]
tags: [rca, p3, application]
status: resolved
duration_minutes: 72
author: SRE
---

# 2025-07-30 - Cache Invalidation Bug in recommendation-engine

## Summary

On 2025-07-30, the recommendation-engine service experienced a cache invalidation bug. The incident lasted approximately 72 minutes and affected 7082 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 20:05 | Monitoring alert triggered |
| 20:07 | On-call engineer paged |
| 20:10 | Initial investigation started |
| 20:15 | Root cause identified |
| 20:48 | Mitigation applied |
| 21:02 | Service recovery observed |
| 21:17 | Incident resolved |

## Root Cause


The incident was caused by cache invalidation bug in the recommendation-engine service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 61% of requests affected
- Error rate spike: 22% (baseline: <1%)
- Latency increase: p99 went from 259ms to 4951ms


### Affected Services
- recommendation-engine
- billing-api

### Customer Impact

- 2090 customer-facing errors
- 30 support tickets created
- Estimated revenue impact: $49804


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 3 minutes of incident start
- On-call response was quick (5 minutes)
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
| P1 | Implement monitoring for cache invalidation bug | DevOps | 2025-08-06 |
| P2 | Update runbook | Platform Engineering | 2025-08-13 |
| P2 | Add load test scenario | Platform Engineering | 2025-08-20 |
| P3 | Review similar services | Backend Team | 2025-08-29 |


## Related Incidents


- [[2025-07-30-previous-incident|Previous application incident]]
- [[runbook-recommendation-engine|recommendation-engine Runbook]]
- [[architecture-application|Application Architecture]]


---
*RCA prepared by SRE on 2025-08-04*
