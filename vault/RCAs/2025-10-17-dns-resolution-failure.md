---
title: "2025-10-17 - DNS Resolution Failure in billing-api"
date: 2025-10-17
severity: P1
services: [billing-api, recommendation-engine, notification-service, payment-gateway]
tags: [rca, p1, network]
status: resolved
duration_minutes: 132
author: Database Team
---

# 2025-10-17 - DNS Resolution Failure in billing-api

## Summary

On 2025-10-17, the billing-api service experienced a dns resolution failure. The incident lasted approximately 132 minutes and affected 3849 users and 4 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 06:04 | Monitoring alert triggered |
| 06:06 | On-call engineer paged |
| 06:09 | Initial investigation started |
| 06:14 | Root cause identified |
| 07:23 | Mitigation applied |
| 07:49 | Service recovery observed |
| 08:16 | Incident resolved |

## Root Cause


The incident was caused by dns resolution failure in the billing-api service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 90% of requests affected
- Error rate spike: 36% (baseline: <1%)
- Latency increase: p99 went from 261ms to 3198ms


### Affected Services
- billing-api
- recommendation-engine
- notification-service
- payment-gateway

### Customer Impact

- 3587 customer-facing errors
- 97 support tickets created
- Estimated revenue impact: $47212


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 2 minutes of incident start
- On-call response was quick (10 minutes)
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
| P1 | Implement monitoring for dns resolution failure | Infrastructure | 2025-10-24 |
| P2 | Update runbook | Infrastructure | 2025-10-31 |
| P2 | Add load test scenario | Platform Engineering | 2025-11-07 |
| P3 | Review similar services | SRE | 2025-11-16 |


## Related Incidents


- [[2025-10-17-previous-incident|Previous network incident]]
- [[runbook-billing-api|billing-api Runbook]]
- [[architecture-network|Network Architecture]]


---
*RCA prepared by Database Team on 2025-10-18*
