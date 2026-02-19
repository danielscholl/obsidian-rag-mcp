---
title: "2025-05-27 - Third-Party API Degradation in payment-gateway"
date: 2025-05-27
severity: P2
services: [billing-api, payment-gateway]
tags: [rca, p2, external]
status: resolved
duration_minutes: 22
author: Backend Team
---

# 2025-05-27 - Third-Party API Degradation in payment-gateway

## Summary

On 2025-05-27, the payment-gateway service experienced a third-party api degradation. The incident lasted approximately 22 minutes and affected 7847 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 08:13 | Monitoring alert triggered |
| 08:15 | On-call engineer paged |
| 08:18 | Initial investigation started |
| 08:23 | Root cause identified |
| 08:26 | Mitigation applied |
| 08:30 | Service recovery observed |
| 08:35 | Incident resolved |

## Root Cause


The incident was caused by third-party api degradation in the payment-gateway service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 100% of requests affected
- Error rate spike: 46% (baseline: <1%)
- Latency increase: p99 went from 404ms to 5439ms


### Affected Services
- billing-api
- payment-gateway

### Customer Impact

- 389 customer-facing errors
- 45 support tickets created
- Estimated revenue impact: $9707


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

- Need better runbooks for external issues
- Monitoring coverage gaps identified
- Load testing should cover this scenario
- Need automated rollback for faster recovery


## Action Items


| Priority | Action | Owner | Due Date |
|----------|--------|-------|----------|
| P1 | Implement monitoring for third-party api degradation | Database Team | 2025-06-03 |
| P2 | Update runbook | Backend Team | 2025-06-10 |
| P2 | Add load test scenario | Infrastructure | 2025-06-17 |
| P3 | Review similar services | Infrastructure | 2025-06-26 |


## Related Incidents


- [[2025-05-27-previous-incident|Previous external incident]]
- [[runbook-payment-gateway|payment-gateway Runbook]]
- [[architecture-external|External Architecture]]


---
*RCA prepared by Backend Team on 2025-06-01*
