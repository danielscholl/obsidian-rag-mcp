---
title: "2025-06-20 - Cache Invalidation Bug in recommendation-engine"
date: 2025-06-20
severity: P3
services: [recommendation-engine, billing-api, analytics-pipeline]
tags: [rca, p3, application]
status: resolved
duration_minutes: 22
author: Infrastructure
---

# 2025-06-20 - Cache Invalidation Bug in recommendation-engine

## Summary

On 2025-06-20, the recommendation-engine service experienced a cache invalidation bug. The incident lasted approximately 22 minutes and affected 682 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 02:26 | Monitoring alert triggered |
| 02:28 | On-call engineer paged |
| 02:31 | Initial investigation started |
| 02:36 | Root cause identified |
| 02:39 | Mitigation applied |
| 02:43 | Service recovery observed |
| 02:48 | Incident resolved |

## Root Cause


The incident was caused by cache invalidation bug in the recommendation-engine service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 87% of requests affected
- Error rate spike: 43% (baseline: <1%)
- Latency increase: p99 went from 130ms to 5051ms


### Affected Services
- recommendation-engine
- billing-api
- analytics-pipeline

### Customer Impact

- 4282 customer-facing errors
- 70 support tickets created
- Estimated revenue impact: $43148


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 5 minutes of incident start
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
| P1 | Implement monitoring for cache invalidation bug | Database Team | 2025-06-27 |
| P2 | Update runbook | Database Team | 2025-07-04 |
| P2 | Add load test scenario | Infrastructure | 2025-07-11 |
| P3 | Review similar services | Database Team | 2025-07-20 |


## Related Incidents


- [[2025-06-20-previous-incident|Previous application incident]]
- [[runbook-recommendation-engine|recommendation-engine Runbook]]
- [[architecture-application|Application Architecture]]


---
*RCA prepared by Infrastructure on 2025-06-25*
