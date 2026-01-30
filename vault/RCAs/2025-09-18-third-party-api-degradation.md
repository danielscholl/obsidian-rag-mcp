---
title: "2025-09-18 - Third-Party API Degradation in payment-gateway"
date: 2025-09-18
severity: P2
services: [auth-service, user-service, payment-gateway]
tags: [rca, p2, external]
status: resolved
duration_minutes: 34
author: Backend Team
---

# 2025-09-18 - Third-Party API Degradation in payment-gateway

## Summary

On 2025-09-18, the payment-gateway service experienced a third-party api degradation. The incident lasted approximately 34 minutes and affected 9674 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 18:05 | Monitoring alert triggered |
| 18:07 | On-call engineer paged |
| 18:10 | Initial investigation started |
| 18:15 | Root cause identified |
| 18:25 | Mitigation applied |
| 18:32 | Service recovery observed |
| 18:39 | Incident resolved |

## Root Cause


The incident was caused by third-party api degradation in the payment-gateway service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 79% of requests affected
- Error rate spike: 35% (baseline: <1%)
- Latency increase: p99 went from 419ms to 3876ms


### Affected Services
- auth-service
- user-service
- payment-gateway

### Customer Impact

- 1070 customer-facing errors
- 61 support tickets created
- Estimated revenue impact: $24038


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

- Need better runbooks for external issues
- Monitoring coverage gaps identified
- Load testing should cover this scenario
- Need automated rollback for faster recovery


## Action Items


| Priority | Action | Owner | Due Date |
|----------|--------|-------|----------|
| P1 | Implement monitoring for third-party api degradation | Database Team | 2025-09-25 |
| P2 | Update runbook | Platform Engineering | 2025-10-02 |
| P2 | Add load test scenario | Infrastructure | 2025-10-09 |
| P3 | Review similar services | Platform Engineering | 2025-10-18 |


## Related Incidents


- [[2025-09-18-previous-incident|Previous external incident]]
- [[runbook-payment-gateway|payment-gateway Runbook]]
- [[architecture-external|External Architecture]]


---
*RCA prepared by Backend Team on 2025-09-22*
