---
title: "2025-12-13 - Message Queue Backlog in search-api"
date: 2025-12-13
severity: P2
services: [search-api, recommendation-engine, billing-api, order-service]
tags: [rca, p2, messaging]
status: resolved
duration_minutes: 17
author: Infrastructure
---

# 2025-12-13 - Message Queue Backlog in search-api

## Summary

On 2025-12-13, the search-api service experienced a message queue backlog. The incident lasted approximately 17 minutes and affected 6753 users and 4 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 08:49 | Monitoring alert triggered |
| 08:51 | On-call engineer paged |
| 08:54 | Initial investigation started |
| 08:59 | Root cause identified |
| 08:59 | Mitigation applied |
| 09:02 | Service recovery observed |
| 09:06 | Incident resolved |

## Root Cause


The incident was caused by message queue backlog in the search-api service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 83% of requests affected
- Error rate spike: 16% (baseline: <1%)
- Latency increase: p99 went from 371ms to 7600ms


### Affected Services
- search-api
- recommendation-engine
- billing-api
- order-service

### Customer Impact

- 1786 customer-facing errors
- 99 support tickets created
- Estimated revenue impact: $22091


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 3 minutes of incident start
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
| P1 | Implement monitoring for message queue backlog | Platform Engineering | 2025-12-20 |
| P2 | Update runbook | Infrastructure | 2025-12-27 |
| P2 | Add load test scenario | Backend Team | 2026-01-03 |
| P3 | Review similar services | Backend Team | 2026-01-12 |


## Related Incidents


- [[2025-12-13-previous-incident|Previous messaging incident]]
- [[runbook-search-api|search-api Runbook]]
- [[architecture-messaging|Messaging Architecture]]


---
*RCA prepared by Infrastructure on 2025-12-15*
