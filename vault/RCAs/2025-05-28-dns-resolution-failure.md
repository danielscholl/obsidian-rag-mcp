---
title: "2025-05-28 - DNS Resolution Failure in billing-api"
date: 2025-05-28
severity: P1
services: [billing-api, recommendation-engine, payment-gateway]
tags: [rca, p1, network]
status: resolved
duration_minutes: 107
author: Backend Team
---

# 2025-05-28 - DNS Resolution Failure in billing-api

## Summary

On 2025-05-28, the billing-api service experienced a dns resolution failure. The incident lasted approximately 107 minutes and affected 7973 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 23:39 | Monitoring alert triggered |
| 23:41 | On-call engineer paged |
| 23:44 | Initial investigation started |
| 23:49 | Root cause identified |
| 00:43 | Mitigation applied |
| 01:04 | Service recovery observed |
| 01:26 | Incident resolved |

## Root Cause


The incident was caused by dns resolution failure in the billing-api service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 70% of requests affected
- Error rate spike: 41% (baseline: <1%)
- Latency increase: p99 went from 167ms to 2944ms


### Affected Services
- billing-api
- recommendation-engine
- payment-gateway

### Customer Impact

- 4583 customer-facing errors
- 76 support tickets created
- Estimated revenue impact: $37664


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 4 minutes of incident start
- On-call response was quick (4 minutes)
- Cross-team collaboration was effective
- Communication to stakeholders was timely


### What Could Be Improved  

- Need better runbooks for network issues
- Monitoring coverage gaps identified
- Load testing should cover this scenario
- Need automated rollback for faster recovery


## Action Items


| Priority | Action | Owner | Due Date |
|----------|--------|-------|----------|
| P1 | Implement monitoring for dns resolution failure | DevOps | 2025-06-04 |
| P2 | Update runbook | DevOps | 2025-06-11 |
| P2 | Add load test scenario | Platform Engineering | 2025-06-18 |
| P3 | Review similar services | Infrastructure | 2025-06-27 |


## Related Incidents


- [[2025-05-28-previous-incident|Previous network incident]]
- [[runbook-billing-api|billing-api Runbook]]
- [[architecture-network|Network Architecture]]


---
*RCA prepared by Backend Team on 2025-05-30*
