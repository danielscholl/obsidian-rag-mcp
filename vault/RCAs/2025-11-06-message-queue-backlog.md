---
title: "2025-11-06 - Message Queue Backlog in payment-gateway"
date: 2025-11-06
severity: P2
services: [payment-gateway, auth-service]
tags: [rca, p2, messaging]
status: resolved
duration_minutes: 32
author: SRE
---

# 2025-11-06 - Message Queue Backlog in payment-gateway

## Summary

On 2025-11-06, the payment-gateway service experienced a message queue backlog. The incident lasted approximately 32 minutes and affected 4674 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 10:56 | Monitoring alert triggered |
| 10:58 | On-call engineer paged |
| 11:01 | Initial investigation started |
| 11:06 | Root cause identified |
| 11:15 | Mitigation applied |
| 11:21 | Service recovery observed |
| 11:28 | Incident resolved |

## Root Cause


The incident was caused by message queue backlog in the payment-gateway service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 57% of requests affected
- Error rate spike: 24% (baseline: <1%)
- Latency increase: p99 went from 109ms to 7698ms


### Affected Services
- payment-gateway
- auth-service

### Customer Impact

- 2734 customer-facing errors
- 96 support tickets created
- Estimated revenue impact: $25839


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 1 minutes of incident start
- On-call response was quick (9 minutes)
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
| P1 | Implement monitoring for message queue backlog | Database Team | 2025-11-13 |
| P2 | Update runbook | DevOps | 2025-11-20 |
| P2 | Add load test scenario | SRE | 2025-11-27 |
| P3 | Review similar services | Backend Team | 2025-12-06 |


## Related Incidents


- [[2025-11-06-previous-incident|Previous messaging incident]]
- [[runbook-payment-gateway|payment-gateway Runbook]]
- [[architecture-messaging|Messaging Architecture]]


---
*RCA prepared by SRE on 2025-11-07*
