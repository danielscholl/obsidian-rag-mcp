---
title: "2025-03-23 - Memory Leak in Service in inventory-api"
date: 2025-03-23
severity: P2
services: [inventory-api, notification-service, analytics-pipeline, recommendation-engine]
tags: [rca, p2, application]
status: resolved
duration_minutes: 164
author: Backend Team
---

# 2025-03-23 - Memory Leak in Service in inventory-api

## Summary

On 2025-03-23, the inventory-api service experienced a memory leak in service. The incident lasted approximately 164 minutes and affected 112 users and 4 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 05:24 | Monitoring alert triggered |
| 05:26 | On-call engineer paged |
| 05:29 | Initial investigation started |
| 05:34 | Root cause identified |
| 07:02 | Mitigation applied |
| 07:35 | Service recovery observed |
| 08:08 | Incident resolved |

## Root Cause


The incident was caused by memory leak in service in the inventory-api service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 83% of requests affected
- Error rate spike: 21% (baseline: <1%)
- Latency increase: p99 went from 338ms to 2956ms


### Affected Services
- inventory-api
- notification-service
- analytics-pipeline
- recommendation-engine

### Customer Impact

- 689 customer-facing errors
- 90 support tickets created
- Estimated revenue impact: $36974


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 5 minutes of incident start
- On-call response was quick (4 minutes)
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
| P1 | Implement monitoring for memory leak in service | Platform Engineering | 2025-03-30 |
| P2 | Update runbook | SRE | 2025-04-06 |
| P2 | Add load test scenario | Platform Engineering | 2025-04-13 |
| P3 | Review similar services | Database Team | 2025-04-22 |


## Related Incidents


- [[2025-03-23-previous-incident|Previous application incident]]
- [[runbook-inventory-api|inventory-api Runbook]]
- [[architecture-application|Application Architecture]]


---
*RCA prepared by Backend Team on 2025-03-25*
