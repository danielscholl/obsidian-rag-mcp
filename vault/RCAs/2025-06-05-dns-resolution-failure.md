---
title: "2025-06-05 - DNS Resolution Failure in payment-gateway"
date: 2025-06-05
severity: P1
services: [payment-gateway, auth-service]
tags: [rca, p1, network]
status: resolved
duration_minutes: 40
author: Platform Engineering
---

# 2025-06-05 - DNS Resolution Failure in payment-gateway

## Summary

On 2025-06-05, the payment-gateway service experienced a dns resolution failure. The incident lasted approximately 40 minutes and affected 8243 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 15:57 | Monitoring alert triggered |
| 15:59 | On-call engineer paged |
| 16:02 | Initial investigation started |
| 16:07 | Root cause identified |
| 16:21 | Mitigation applied |
| 16:29 | Service recovery observed |
| 16:37 | Incident resolved |

## Root Cause


The incident was caused by dns resolution failure in the payment-gateway service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 71% of requests affected
- Error rate spike: 44% (baseline: <1%)
- Latency increase: p99 went from 301ms to 8993ms


### Affected Services
- payment-gateway
- auth-service

### Customer Impact

- 172 customer-facing errors
- 35 support tickets created
- Estimated revenue impact: $11629


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 3 minutes of incident start
- On-call response was quick (6 minutes)
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
| P1 | Implement monitoring for dns resolution failure | Platform Engineering | 2025-06-12 |
| P2 | Update runbook | Database Team | 2025-06-19 |
| P2 | Add load test scenario | DevOps | 2025-06-26 |
| P3 | Review similar services | SRE | 2025-07-05 |


## Related Incidents


- [[2025-06-05-previous-incident|Previous network incident]]
- [[runbook-payment-gateway|payment-gateway Runbook]]
- [[architecture-network|Network Architecture]]


---
*RCA prepared by Platform Engineering on 2025-06-06*
