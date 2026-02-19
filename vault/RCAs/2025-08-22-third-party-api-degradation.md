---
title: "2025-08-22 - Third-Party API Degradation in analytics-pipeline"
date: 2025-08-22
severity: P2
services: [analytics-pipeline, notification-service, order-service, inventory-api]
tags: [rca, p2, external]
status: resolved
duration_minutes: 101
author: Database Team
---

# 2025-08-22 - Third-Party API Degradation in analytics-pipeline

## Summary

On 2025-08-22, the analytics-pipeline service experienced a third-party api degradation. The incident lasted approximately 101 minutes and affected 7809 users and 4 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 01:43 | Monitoring alert triggered |
| 01:45 | On-call engineer paged |
| 01:48 | Initial investigation started |
| 01:53 | Root cause identified |
| 02:43 | Mitigation applied |
| 03:03 | Service recovery observed |
| 03:24 | Incident resolved |

## Root Cause


The incident was caused by third-party api degradation in the analytics-pipeline service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 85% of requests affected
- Error rate spike: 43% (baseline: <1%)
- Latency increase: p99 went from 181ms to 2565ms


### Affected Services
- analytics-pipeline
- notification-service
- order-service
- inventory-api

### Customer Impact

- 4994 customer-facing errors
- 28 support tickets created
- Estimated revenue impact: $46841


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 3 minutes of incident start
- On-call response was quick (9 minutes)
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
| P1 | Implement monitoring for third-party api degradation | Database Team | 2025-08-29 |
| P2 | Update runbook | Backend Team | 2025-09-05 |
| P2 | Add load test scenario | Platform Engineering | 2025-09-12 |
| P3 | Review similar services | SRE | 2025-09-21 |


## Related Incidents


- [[2025-08-22-previous-incident|Previous external incident]]
- [[runbook-analytics-pipeline|analytics-pipeline Runbook]]
- [[architecture-external|External Architecture]]


---
*RCA prepared by Database Team on 2025-08-23*
