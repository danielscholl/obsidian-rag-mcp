---
title: "2025-11-01 - Rate Limiting Triggered in recommendation-engine"
date: 2025-11-01
severity: P3
services: [notification-service, recommendation-engine]
tags: [rca, p3, application]
status: resolved
duration_minutes: 57
author: Platform Engineering
---

# 2025-11-01 - Rate Limiting Triggered in recommendation-engine

## Summary

On 2025-11-01, the recommendation-engine service experienced a rate limiting triggered. The incident lasted approximately 57 minutes and affected 9148 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 18:04 | Monitoring alert triggered |
| 18:06 | On-call engineer paged |
| 18:09 | Initial investigation started |
| 18:14 | Root cause identified |
| 18:38 | Mitigation applied |
| 18:49 | Service recovery observed |
| 19:01 | Incident resolved |

## Root Cause


The incident was caused by rate limiting triggered in the recommendation-engine service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 89% of requests affected
- Error rate spike: 40% (baseline: <1%)
- Latency increase: p99 went from 240ms to 2877ms


### Affected Services
- notification-service
- recommendation-engine

### Customer Impact

- 2353 customer-facing errors
- 29 support tickets created
- Estimated revenue impact: $29602


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 2 minutes of incident start
- On-call response was quick (9 minutes)
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
| P1 | Implement monitoring for rate limiting triggered | Database Team | 2025-11-08 |
| P2 | Update runbook | Backend Team | 2025-11-15 |
| P2 | Add load test scenario | Infrastructure | 2025-11-22 |
| P3 | Review similar services | SRE | 2025-12-01 |


## Related Incidents


- [[2025-11-01-previous-incident|Previous application incident]]
- [[runbook-recommendation-engine|recommendation-engine Runbook]]
- [[architecture-application|Application Architecture]]


---
*RCA prepared by Platform Engineering on 2025-11-04*
