---
title: "2025-06-20 - Deployment Rollback Required in payment-gateway"
date: 2025-06-20
severity: P2
services: [payment-gateway, order-service, recommendation-engine, search-api]
tags: [rca, p2, deployment]
status: resolved
duration_minutes: 160
author: SRE
---

# 2025-06-20 - Deployment Rollback Required in payment-gateway

## Summary

On 2025-06-20, the payment-gateway service experienced a deployment rollback required. The incident lasted approximately 160 minutes and affected 5950 users and 4 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 08:18 | Monitoring alert triggered |
| 08:20 | On-call engineer paged |
| 08:23 | Initial investigation started |
| 08:28 | Root cause identified |
| 09:54 | Mitigation applied |
| 10:26 | Service recovery observed |
| 10:58 | Incident resolved |

## Root Cause


The incident was caused by deployment rollback required in the payment-gateway service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 51% of requests affected
- Error rate spike: 24% (baseline: <1%)
- Latency increase: p99 went from 422ms to 2193ms


### Affected Services
- payment-gateway
- order-service
- recommendation-engine
- search-api

### Customer Impact

- 4343 customer-facing errors
- 59 support tickets created
- Estimated revenue impact: $34546


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 1 minutes of incident start
- On-call response was quick (4 minutes)
- Cross-team collaboration was effective
- Communication to stakeholders was timely


### What Could Be Improved  

- Need better runbooks for deployment issues
- Monitoring coverage gaps identified
- Load testing should cover this scenario
- Need automated rollback for faster recovery


## Action Items


| Priority | Action | Owner | Due Date |
|----------|--------|-------|----------|
| P1 | Implement monitoring for deployment rollback required | DevOps | 2025-06-27 |
| P2 | Update runbook | Backend Team | 2025-07-04 |
| P2 | Add load test scenario | Backend Team | 2025-07-11 |
| P3 | Review similar services | DevOps | 2025-07-20 |


## Related Incidents


- [[2025-06-20-previous-incident|Previous deployment incident]]
- [[runbook-payment-gateway|payment-gateway Runbook]]
- [[architecture-deployment|Deployment Architecture]]


---
*RCA prepared by SRE on 2025-06-24*
