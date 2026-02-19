---
title: "2025-08-15 - Message Queue Backlog in billing-api"
date: 2025-08-15
severity: P2
services: [billing-api, auth-service]
tags: [rca, p2, messaging]
status: resolved
duration_minutes: 101
author: Database Team
---

# 2025-08-15 - Message Queue Backlog in billing-api

## Summary

On 2025-08-15, the billing-api service experienced a message queue backlog. The incident lasted approximately 101 minutes and affected 2366 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 22:29 | Monitoring alert triggered |
| 22:31 | On-call engineer paged |
| 22:34 | Initial investigation started |
| 22:39 | Root cause identified |
| 23:29 | Mitigation applied |
| 23:49 | Service recovery observed |
| 00:10 | Incident resolved |

## Root Cause


The incident was caused by message queue backlog in the billing-api service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 100% of requests affected
- Error rate spike: 31% (baseline: <1%)
- Latency increase: p99 went from 465ms to 3061ms


### Affected Services
- billing-api
- auth-service

### Customer Impact

- 2398 customer-facing errors
- 63 support tickets created
- Estimated revenue impact: $32153


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 1 minutes of incident start
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
| P1 | Implement monitoring for message queue backlog | Database Team | 2025-08-22 |
| P2 | Update runbook | Platform Engineering | 2025-08-29 |
| P2 | Add load test scenario | DevOps | 2025-09-05 |
| P3 | Review similar services | Database Team | 2025-09-14 |


## Related Incidents


- [[2025-08-15-previous-incident|Previous messaging incident]]
- [[runbook-billing-api|billing-api Runbook]]
- [[architecture-messaging|Messaging Architecture]]


---
*RCA prepared by Database Team on 2025-08-17*
