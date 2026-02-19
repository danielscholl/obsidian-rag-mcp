---
title: "2025-12-07 - Message Queue Backlog in auth-service"
date: 2025-12-07
severity: P2
services: [auth-service, user-service, analytics-pipeline]
tags: [rca, p2, messaging]
status: resolved
duration_minutes: 58
author: Backend Team
---

# 2025-12-07 - Message Queue Backlog in auth-service

## Summary

On 2025-12-07, the auth-service service experienced a message queue backlog. The incident lasted approximately 58 minutes and affected 6900 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 18:23 | Monitoring alert triggered |
| 18:25 | On-call engineer paged |
| 18:28 | Initial investigation started |
| 18:33 | Root cause identified |
| 18:57 | Mitigation applied |
| 19:09 | Service recovery observed |
| 19:21 | Incident resolved |

## Root Cause


The incident was caused by message queue backlog in the auth-service service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 90% of requests affected
- Error rate spike: 37% (baseline: <1%)
- Latency increase: p99 went from 258ms to 4178ms


### Affected Services
- auth-service
- user-service
- analytics-pipeline

### Customer Impact

- 3897 customer-facing errors
- 26 support tickets created
- Estimated revenue impact: $38325


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 4 minutes of incident start
- On-call response was quick (7 minutes)
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
| P1 | Implement monitoring for message queue backlog | Platform Engineering | 2025-12-14 |
| P2 | Update runbook | Database Team | 2025-12-21 |
| P2 | Add load test scenario | Backend Team | 2025-12-28 |
| P3 | Review similar services | Infrastructure | 2026-01-06 |


## Related Incidents


- [[2025-12-07-previous-incident|Previous messaging incident]]
- [[runbook-auth-service|auth-service Runbook]]
- [[architecture-messaging|Messaging Architecture]]


---
*RCA prepared by Backend Team on 2025-12-10*
