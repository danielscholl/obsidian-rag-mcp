---
title: "2025-08-21 - Third-Party API Degradation in analytics-pipeline"
date: 2025-08-21
severity: P2
services: [analytics-pipeline, notification-service]
tags: [rca, p2, external]
status: resolved
duration_minutes: 61
author: DevOps
---

# 2025-08-21 - Third-Party API Degradation in analytics-pipeline

## Summary

On 2025-08-21, the analytics-pipeline service experienced a third-party api degradation. The incident lasted approximately 61 minutes and affected 584 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 23:08 | Monitoring alert triggered |
| 23:10 | On-call engineer paged |
| 23:13 | Initial investigation started |
| 23:18 | Root cause identified |
| 23:44 | Mitigation applied |
| 23:56 | Service recovery observed |
| 00:09 | Incident resolved |

## Root Cause


The incident was caused by third-party api degradation in the analytics-pipeline service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 97% of requests affected
- Error rate spike: 11% (baseline: <1%)
- Latency increase: p99 went from 414ms to 4063ms


### Affected Services
- analytics-pipeline
- notification-service

### Customer Impact

- 2651 customer-facing errors
- 80 support tickets created
- Estimated revenue impact: $6119


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

- Need better runbooks for external issues
- Monitoring coverage gaps identified
- Load testing should cover this scenario
- Need automated rollback for faster recovery


## Action Items


| Priority | Action | Owner | Due Date |
|----------|--------|-------|----------|
| P1 | Implement monitoring for third-party api degradation | DevOps | 2025-08-28 |
| P2 | Update runbook | Platform Engineering | 2025-09-04 |
| P2 | Add load test scenario | DevOps | 2025-09-11 |
| P3 | Review similar services | Platform Engineering | 2025-09-20 |


## Related Incidents


- [[2025-08-21-previous-incident|Previous external incident]]
- [[runbook-analytics-pipeline|analytics-pipeline Runbook]]
- [[architecture-external|External Architecture]]


---
*RCA prepared by DevOps on 2025-08-23*
