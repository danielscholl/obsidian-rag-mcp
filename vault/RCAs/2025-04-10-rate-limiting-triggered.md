---
title: "2025-04-10 - Rate Limiting Triggered in inventory-api"
date: 2025-04-10
severity: P3
services: [inventory-api, analytics-pipeline, order-service]
tags: [rca, p3, application]
status: resolved
duration_minutes: 100
author: Backend Team
---

# 2025-04-10 - Rate Limiting Triggered in inventory-api

## Summary

On 2025-04-10, the inventory-api service experienced a rate limiting triggered. The incident lasted approximately 100 minutes and affected 5965 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 23:35 | Monitoring alert triggered |
| 23:37 | On-call engineer paged |
| 23:40 | Initial investigation started |
| 23:45 | Root cause identified |
| 00:35 | Mitigation applied |
| 00:55 | Service recovery observed |
| 01:15 | Incident resolved |

## Root Cause


The incident was caused by rate limiting triggered in the inventory-api service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 98% of requests affected
- Error rate spike: 43% (baseline: <1%)
- Latency increase: p99 went from 423ms to 4979ms


### Affected Services
- inventory-api
- analytics-pipeline
- order-service

### Customer Impact

- 2370 customer-facing errors
- 45 support tickets created
- Estimated revenue impact: $26521


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 5 minutes of incident start
- On-call response was quick (3 minutes)
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
| P1 | Implement monitoring for rate limiting triggered | Backend Team | 2025-04-17 |
| P2 | Update runbook | DevOps | 2025-04-24 |
| P2 | Add load test scenario | Backend Team | 2025-05-01 |
| P3 | Review similar services | DevOps | 2025-05-10 |


## Related Incidents


- [[2025-04-10-previous-incident|Previous application incident]]
- [[runbook-inventory-api|inventory-api Runbook]]
- [[architecture-application|Application Architecture]]


---
*RCA prepared by Backend Team on 2025-04-13*
