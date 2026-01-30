---
title: "2025-05-10 - Memory Leak in Service in notification-service"
date: 2025-05-10
severity: P2
services: [notification-service, recommendation-engine, inventory-api]
tags: [rca, p2, application]
status: resolved
duration_minutes: 133
author: Infrastructure
---

# 2025-05-10 - Memory Leak in Service in notification-service

## Summary

On 2025-05-10, the notification-service service experienced a memory leak in service. The incident lasted approximately 133 minutes and affected 8349 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 10:18 | Monitoring alert triggered |
| 10:20 | On-call engineer paged |
| 10:23 | Initial investigation started |
| 10:28 | Root cause identified |
| 11:37 | Mitigation applied |
| 12:04 | Service recovery observed |
| 12:31 | Incident resolved |

## Root Cause


The incident was caused by memory leak in service in the notification-service service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 64% of requests affected
- Error rate spike: 18% (baseline: <1%)
- Latency increase: p99 went from 167ms to 5812ms


### Affected Services
- notification-service
- recommendation-engine
- inventory-api

### Customer Impact

- 2673 customer-facing errors
- 56 support tickets created
- Estimated revenue impact: $24908


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
| P1 | Implement monitoring for memory leak in service | Infrastructure | 2025-05-17 |
| P2 | Update runbook | SRE | 2025-05-24 |
| P2 | Add load test scenario | Infrastructure | 2025-05-31 |
| P3 | Review similar services | Infrastructure | 2025-06-09 |


## Related Incidents


- [[2025-05-10-previous-incident|Previous application incident]]
- [[runbook-notification-service|notification-service Runbook]]
- [[architecture-application|Application Architecture]]


---
*RCA prepared by Infrastructure on 2025-05-11*
