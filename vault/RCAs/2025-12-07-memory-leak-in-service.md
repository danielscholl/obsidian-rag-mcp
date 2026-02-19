---
title: "2025-12-07 - Memory Leak in Service in auth-service"
date: 2025-12-07
severity: P2
services: [auth-service, payment-gateway, order-service]
tags: [rca, p2, application]
status: resolved
duration_minutes: 114
author: Backend Team
---

# 2025-12-07 - Memory Leak in Service in auth-service

## Summary

On 2025-12-07, the auth-service service experienced a memory leak in service. The incident lasted approximately 114 minutes and affected 8962 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 15:50 | Monitoring alert triggered |
| 15:52 | On-call engineer paged |
| 15:55 | Initial investigation started |
| 16:00 | Root cause identified |
| 16:58 | Mitigation applied |
| 17:21 | Service recovery observed |
| 17:44 | Incident resolved |

## Root Cause


The incident was caused by memory leak in service in the auth-service service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 86% of requests affected
- Error rate spike: 33% (baseline: <1%)
- Latency increase: p99 went from 344ms to 4016ms


### Affected Services
- auth-service
- payment-gateway
- order-service

### Customer Impact

- 1045 customer-facing errors
- 68 support tickets created
- Estimated revenue impact: $30520


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 2 minutes of incident start
- On-call response was quick (4 minutes)
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
| P1 | Implement monitoring for memory leak in service | Platform Engineering | 2025-12-14 |
| P2 | Update runbook | Platform Engineering | 2025-12-21 |
| P2 | Add load test scenario | Platform Engineering | 2025-12-28 |
| P3 | Review similar services | Database Team | 2026-01-06 |


## Related Incidents


- [[2025-12-07-previous-incident|Previous application incident]]
- [[runbook-auth-service|auth-service Runbook]]
- [[architecture-application|Application Architecture]]


---
*RCA prepared by Backend Team on 2025-12-11*
