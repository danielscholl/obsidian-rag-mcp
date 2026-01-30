---
title: "2025-12-27 - Message Queue Backlog in analytics-pipeline"
date: 2025-12-27
severity: P2
services: [analytics-pipeline, order-service]
tags: [rca, p2, messaging]
status: resolved
duration_minutes: 166
author: Backend Team
---

# 2025-12-27 - Message Queue Backlog in analytics-pipeline

## Summary

On 2025-12-27, the analytics-pipeline service experienced a message queue backlog. The incident lasted approximately 166 minutes and affected 8783 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 21:30 | Monitoring alert triggered |
| 21:32 | On-call engineer paged |
| 21:35 | Initial investigation started |
| 21:40 | Root cause identified |
| 23:09 | Mitigation applied |
| 23:42 | Service recovery observed |
| 00:16 | Incident resolved |

## Root Cause


The incident was caused by message queue backlog in the analytics-pipeline service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 66% of requests affected
- Error rate spike: 28% (baseline: <1%)
- Latency increase: p99 went from 487ms to 8177ms


### Affected Services
- analytics-pipeline
- order-service

### Customer Impact

- 4291 customer-facing errors
- 51 support tickets created
- Estimated revenue impact: $29819


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 5 minutes of incident start
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
| P1 | Implement monitoring for message queue backlog | Database Team | 2026-01-03 |
| P2 | Update runbook | Backend Team | 2026-01-10 |
| P2 | Add load test scenario | Database Team | 2026-01-17 |
| P3 | Review similar services | Backend Team | 2026-01-26 |


## Related Incidents


- [[2025-12-27-previous-incident|Previous messaging incident]]
- [[runbook-analytics-pipeline|analytics-pipeline Runbook]]
- [[architecture-messaging|Messaging Architecture]]


---
*RCA prepared by Backend Team on 2025-12-28*
