---
title: "2025-04-17 - Third-Party API Degradation in analytics-pipeline"
date: 2025-04-17
severity: P2
services: [analytics-pipeline, inventory-api, recommendation-engine]
tags: [rca, p2, external]
status: resolved
duration_minutes: 180
author: SRE
---

# 2025-04-17 - Third-Party API Degradation in analytics-pipeline

## Summary

On 2025-04-17, the analytics-pipeline service experienced a third-party api degradation. The incident lasted approximately 180 minutes and affected 6584 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 10:18 | Monitoring alert triggered |
| 10:20 | On-call engineer paged |
| 10:23 | Initial investigation started |
| 10:28 | Root cause identified |
| 12:06 | Mitigation applied |
| 12:42 | Service recovery observed |
| 13:18 | Incident resolved |

## Root Cause


The incident was caused by third-party api degradation in the analytics-pipeline service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 51% of requests affected
- Error rate spike: 14% (baseline: <1%)
- Latency increase: p99 went from 272ms to 5047ms


### Affected Services
- analytics-pipeline
- inventory-api
- recommendation-engine

### Customer Impact

- 3445 customer-facing errors
- 18 support tickets created
- Estimated revenue impact: $8492


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

- Need better runbooks for external issues
- Monitoring coverage gaps identified
- Load testing should cover this scenario
- Need automated rollback for faster recovery


## Action Items


| Priority | Action | Owner | Due Date |
|----------|--------|-------|----------|
| P1 | Implement monitoring for third-party api degradation | DevOps | 2025-04-24 |
| P2 | Update runbook | Infrastructure | 2025-05-01 |
| P2 | Add load test scenario | DevOps | 2025-05-08 |
| P3 | Review similar services | Database Team | 2025-05-17 |


## Related Incidents


- [[2025-04-17-previous-incident|Previous external incident]]
- [[runbook-analytics-pipeline|analytics-pipeline Runbook]]
- [[architecture-external|External Architecture]]


---
*RCA prepared by SRE on 2025-04-22*
