---
title: "2025-06-10 - Cache Invalidation Bug in payment-gateway"
date: 2025-06-10
severity: P3
services: [recommendation-engine, billing-api, payment-gateway]
tags: [rca, p3, application]
status: resolved
duration_minutes: 92
author: Backend Team
---

# 2025-06-10 - Cache Invalidation Bug in payment-gateway

## Summary

On 2025-06-10, the payment-gateway service experienced a cache invalidation bug. The incident lasted approximately 92 minutes and affected 155 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 02:23 | Monitoring alert triggered |
| 02:25 | On-call engineer paged |
| 02:28 | Initial investigation started |
| 02:33 | Root cause identified |
| 03:18 | Mitigation applied |
| 03:36 | Service recovery observed |
| 03:55 | Incident resolved |

## Root Cause


The incident was caused by cache invalidation bug in the payment-gateway service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 83% of requests affected
- Error rate spike: 29% (baseline: <1%)
- Latency increase: p99 went from 399ms to 4902ms


### Affected Services
- recommendation-engine
- billing-api
- payment-gateway

### Customer Impact

- 1331 customer-facing errors
- 76 support tickets created
- Estimated revenue impact: $48498


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 4 minutes of incident start
- On-call response was quick (8 minutes)
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
| P1 | Implement monitoring for cache invalidation bug | Infrastructure | 2025-06-17 |
| P2 | Update runbook | DevOps | 2025-06-24 |
| P2 | Add load test scenario | Database Team | 2025-07-01 |
| P3 | Review similar services | DevOps | 2025-07-10 |


## Related Incidents


- [[2025-06-10-previous-incident|Previous application incident]]
- [[runbook-payment-gateway|payment-gateway Runbook]]
- [[architecture-application|Application Architecture]]


---
*RCA prepared by Backend Team on 2025-06-12*
