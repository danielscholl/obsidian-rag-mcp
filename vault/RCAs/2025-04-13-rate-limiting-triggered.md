---
title: "2025-04-13 - Rate Limiting Triggered in billing-api"
date: 2025-04-13
severity: P3
services: [billing-api, analytics-pipeline, auth-service, order-service]
tags: [rca, p3, application]
status: resolved
duration_minutes: 47
author: Backend Team
---

# 2025-04-13 - Rate Limiting Triggered in billing-api

## Summary

On 2025-04-13, the billing-api service experienced a rate limiting triggered. The incident lasted approximately 47 minutes and affected 5835 users and 4 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 21:16 | Monitoring alert triggered |
| 21:18 | On-call engineer paged |
| 21:21 | Initial investigation started |
| 21:26 | Root cause identified |
| 21:44 | Mitigation applied |
| 21:53 | Service recovery observed |
| 22:03 | Incident resolved |

## Root Cause


The incident was caused by rate limiting triggered in the billing-api service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 83% of requests affected
- Error rate spike: 20% (baseline: <1%)
- Latency increase: p99 went from 348ms to 6238ms


### Affected Services
- billing-api
- analytics-pipeline
- auth-service
- order-service

### Customer Impact

- 1045 customer-facing errors
- 94 support tickets created
- Estimated revenue impact: $27327


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 2 minutes of incident start
- On-call response was quick (2 minutes)
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
| P1 | Implement monitoring for rate limiting triggered | Platform Engineering | 2025-04-20 |
| P2 | Update runbook | Platform Engineering | 2025-04-27 |
| P2 | Add load test scenario | DevOps | 2025-05-04 |
| P3 | Review similar services | Platform Engineering | 2025-05-13 |


## Related Incidents


- [[2025-04-13-previous-incident|Previous application incident]]
- [[runbook-billing-api|billing-api Runbook]]
- [[architecture-application|Application Architecture]]


---
*RCA prepared by Backend Team on 2025-04-17*
