---
title: "2026-01-08 - Third-Party API Degradation in analytics-pipeline"
date: 2026-01-08
severity: P2
services: [notification-service, analytics-pipeline, recommendation-engine]
tags: [rca, p2, external]
status: resolved
duration_minutes: 55
author: Backend Team
---

# 2026-01-08 - Third-Party API Degradation in analytics-pipeline

## Summary

On 2026-01-08, the analytics-pipeline service experienced a third-party api degradation. The incident lasted approximately 55 minutes and affected 561 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 12:42 | Monitoring alert triggered |
| 12:44 | On-call engineer paged |
| 12:47 | Initial investigation started |
| 12:52 | Root cause identified |
| 13:15 | Mitigation applied |
| 13:26 | Service recovery observed |
| 13:37 | Incident resolved |

## Root Cause


The incident was caused by third-party api degradation in the analytics-pipeline service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 76% of requests affected
- Error rate spike: 44% (baseline: <1%)
- Latency increase: p99 went from 151ms to 8179ms


### Affected Services
- notification-service
- analytics-pipeline
- recommendation-engine

### Customer Impact

- 194 customer-facing errors
- 67 support tickets created
- Estimated revenue impact: $40715


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 5 minutes of incident start
- On-call response was quick (3 minutes)
- Cross-team collaboration was effective
- Communication to stakeholders was timely


### What Could Be Improved  

- Need better runbooks for external issues
- Monitoring coverage gaps identified
- Load testing should cover this scenario
- Need automated rollback for faster recovery


## Action Items


| Priority | Action | Owner | Due Date |
|----------|--------|-------|----------|
| P1 | Implement monitoring for third-party api degradation | Backend Team | 2026-01-15 |
| P2 | Update runbook | Infrastructure | 2026-01-22 |
| P2 | Add load test scenario | Infrastructure | 2026-01-29 |
| P3 | Review similar services | Platform Engineering | 2026-02-07 |


## Related Incidents


- [[2026-01-08-previous-incident|Previous external incident]]
- [[runbook-analytics-pipeline|analytics-pipeline Runbook]]
- [[architecture-external|External Architecture]]


---
*RCA prepared by Backend Team on 2026-01-12*
