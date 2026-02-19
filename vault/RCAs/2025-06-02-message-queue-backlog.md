---
title: "2025-06-02 - Message Queue Backlog in inventory-api"
date: 2025-06-02
severity: P2
services: [inventory-api, billing-api]
tags: [rca, p2, messaging]
status: resolved
duration_minutes: 65
author: Platform Engineering
---

# 2025-06-02 - Message Queue Backlog in inventory-api

## Summary

On 2025-06-02, the inventory-api service experienced a message queue backlog. The incident lasted approximately 65 minutes and affected 1348 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 15:53 | Monitoring alert triggered |
| 15:55 | On-call engineer paged |
| 15:58 | Initial investigation started |
| 16:03 | Root cause identified |
| 16:32 | Mitigation applied |
| 16:45 | Service recovery observed |
| 16:58 | Incident resolved |

## Root Cause


The incident was caused by message queue backlog in the inventory-api service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 82% of requests affected
- Error rate spike: 18% (baseline: <1%)
- Latency increase: p99 went from 299ms to 7947ms


### Affected Services
- inventory-api
- billing-api

### Customer Impact

- 386 customer-facing errors
- 89 support tickets created
- Estimated revenue impact: $31442


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 3 minutes of incident start
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
| P1 | Implement monitoring for message queue backlog | SRE | 2025-06-09 |
| P2 | Update runbook | Platform Engineering | 2025-06-16 |
| P2 | Add load test scenario | Database Team | 2025-06-23 |
| P3 | Review similar services | Infrastructure | 2025-07-02 |


## Related Incidents


- [[2025-06-02-previous-incident|Previous messaging incident]]
- [[runbook-inventory-api|inventory-api Runbook]]
- [[architecture-messaging|Messaging Architecture]]


---
*RCA prepared by Platform Engineering on 2025-06-04*
