---
title: "2025-03-27 - Memory Leak in Service in inventory-api"
date: 2025-03-27
severity: P2
services: [inventory-api, notification-service, billing-api, order-service]
tags: [rca, p2, application]
status: resolved
duration_minutes: 68
author: Platform Engineering
---

# 2025-03-27 - Memory Leak in Service in inventory-api

## Summary

On 2025-03-27, the inventory-api service experienced a memory leak in service. The incident lasted approximately 68 minutes and affected 3137 users and 4 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 16:14 | Monitoring alert triggered |
| 16:16 | On-call engineer paged |
| 16:19 | Initial investigation started |
| 16:24 | Root cause identified |
| 16:54 | Mitigation applied |
| 17:08 | Service recovery observed |
| 17:22 | Incident resolved |

## Root Cause


The incident was caused by memory leak in service in the inventory-api service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 88% of requests affected
- Error rate spike: 42% (baseline: <1%)
- Latency increase: p99 went from 362ms to 7176ms


### Affected Services
- inventory-api
- notification-service
- billing-api
- order-service

### Customer Impact

- 4215 customer-facing errors
- 38 support tickets created
- Estimated revenue impact: $12658


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 3 minutes of incident start
- On-call response was quick (8 minutes)
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
| P1 | Implement monitoring for memory leak in service | DevOps | 2025-04-03 |
| P2 | Update runbook | Database Team | 2025-04-10 |
| P2 | Add load test scenario | SRE | 2025-04-17 |
| P3 | Review similar services | Platform Engineering | 2025-04-26 |


## Related Incidents


- [[2025-03-27-previous-incident|Previous application incident]]
- [[runbook-inventory-api|inventory-api Runbook]]
- [[architecture-application|Application Architecture]]


---
*RCA prepared by Platform Engineering on 2025-03-29*
