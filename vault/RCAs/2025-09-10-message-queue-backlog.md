---
title: "2025-09-10 - Message Queue Backlog in payment-gateway"
date: 2025-09-10
severity: P2
services: [payment-gateway, billing-api, user-service]
tags: [rca, p2, messaging]
status: resolved
duration_minutes: 86
author: SRE
---

# 2025-09-10 - Message Queue Backlog in payment-gateway

## Summary

On 2025-09-10, the payment-gateway service experienced a message queue backlog. The incident lasted approximately 86 minutes and affected 9431 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 20:01 | Monitoring alert triggered |
| 20:03 | On-call engineer paged |
| 20:06 | Initial investigation started |
| 20:11 | Root cause identified |
| 20:52 | Mitigation applied |
| 21:09 | Service recovery observed |
| 21:27 | Incident resolved |

## Root Cause


The incident was caused by message queue backlog in the payment-gateway service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 74% of requests affected
- Error rate spike: 14% (baseline: <1%)
- Latency increase: p99 went from 247ms to 2317ms


### Affected Services
- payment-gateway
- billing-api
- user-service

### Customer Impact

- 3566 customer-facing errors
- 37 support tickets created
- Estimated revenue impact: $42804


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 1 minutes of incident start
- On-call response was quick (3 minutes)
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
| P1 | Implement monitoring for message queue backlog | Infrastructure | 2025-09-17 |
| P2 | Update runbook | DevOps | 2025-09-24 |
| P2 | Add load test scenario | Backend Team | 2025-10-01 |
| P3 | Review similar services | Backend Team | 2025-10-10 |


## Related Incidents


- [[2025-09-10-previous-incident|Previous messaging incident]]
- [[runbook-payment-gateway|payment-gateway Runbook]]
- [[architecture-messaging|Messaging Architecture]]


---
*RCA prepared by SRE on 2025-09-12*
