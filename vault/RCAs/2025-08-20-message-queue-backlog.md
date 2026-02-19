---
title: "2025-08-20 - Message Queue Backlog in order-service"
date: 2025-08-20
severity: P2
services: [order-service, inventory-api, billing-api]
tags: [rca, p2, messaging]
status: resolved
duration_minutes: 140
author: Database Team
---

# 2025-08-20 - Message Queue Backlog in order-service

## Summary

On 2025-08-20, the order-service service experienced a message queue backlog. The incident lasted approximately 140 minutes and affected 8049 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 18:15 | Monitoring alert triggered |
| 18:17 | On-call engineer paged |
| 18:20 | Initial investigation started |
| 18:25 | Root cause identified |
| 19:39 | Mitigation applied |
| 20:07 | Service recovery observed |
| 20:35 | Incident resolved |

## Root Cause


The incident was caused by message queue backlog in the order-service service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 89% of requests affected
- Error rate spike: 21% (baseline: <1%)
- Latency increase: p99 went from 155ms to 6418ms


### Affected Services
- order-service
- inventory-api
- billing-api

### Customer Impact

- 395 customer-facing errors
- 32 support tickets created
- Estimated revenue impact: $29273


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

- Need better runbooks for messaging issues
- Monitoring coverage gaps identified
- Load testing should cover this scenario
- Need automated rollback for faster recovery


## Action Items


| Priority | Action | Owner | Due Date |
|----------|--------|-------|----------|
| P1 | Implement monitoring for message queue backlog | SRE | 2025-08-27 |
| P2 | Update runbook | SRE | 2025-09-03 |
| P2 | Add load test scenario | DevOps | 2025-09-10 |
| P3 | Review similar services | DevOps | 2025-09-19 |


## Related Incidents


- [[2025-08-20-previous-incident|Previous messaging incident]]
- [[runbook-order-service|order-service Runbook]]
- [[architecture-messaging|Messaging Architecture]]


---
*RCA prepared by Database Team on 2025-08-25*
