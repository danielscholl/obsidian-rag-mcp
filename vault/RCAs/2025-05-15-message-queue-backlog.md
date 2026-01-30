---
title: "2025-05-15 - Message Queue Backlog in order-service"
date: 2025-05-15
severity: P2
services: [order-service, user-service, billing-api, auth-service]
tags: [rca, p2, messaging]
status: resolved
duration_minutes: 48
author: SRE
---

# 2025-05-15 - Message Queue Backlog in order-service

## Summary

On 2025-05-15, the order-service service experienced a message queue backlog. The incident lasted approximately 48 minutes and affected 2389 users and 4 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 14:28 | Monitoring alert triggered |
| 14:30 | On-call engineer paged |
| 14:33 | Initial investigation started |
| 14:38 | Root cause identified |
| 14:56 | Mitigation applied |
| 15:06 | Service recovery observed |
| 15:16 | Incident resolved |

## Root Cause


The incident was caused by message queue backlog in the order-service service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 99% of requests affected
- Error rate spike: 31% (baseline: <1%)
- Latency increase: p99 went from 445ms to 8040ms


### Affected Services
- order-service
- user-service
- billing-api
- auth-service

### Customer Impact

- 1312 customer-facing errors
- 45 support tickets created
- Estimated revenue impact: $30330


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

- Need better runbooks for messaging issues
- Monitoring coverage gaps identified
- Load testing should cover this scenario
- Need automated rollback for faster recovery


## Action Items


| Priority | Action | Owner | Due Date |
|----------|--------|-------|----------|
| P1 | Implement monitoring for message queue backlog | Backend Team | 2025-05-22 |
| P2 | Update runbook | Backend Team | 2025-05-29 |
| P2 | Add load test scenario | Infrastructure | 2025-06-05 |
| P3 | Review similar services | Backend Team | 2025-06-14 |


## Related Incidents


- [[2025-05-15-previous-incident|Previous messaging incident]]
- [[runbook-order-service|order-service Runbook]]
- [[architecture-messaging|Messaging Architecture]]


---
*RCA prepared by SRE on 2025-05-17*
