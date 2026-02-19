---
title: "2025-11-07 - SSL/TLS Handshake Failure in order-service"
date: 2025-11-07
severity: P2
services: [order-service, notification-service, billing-api]
tags: [rca, p2, network]
status: resolved
duration_minutes: 32
author: SRE
---

# 2025-11-07 - SSL/TLS Handshake Failure in order-service

## Summary

On 2025-11-07, the order-service service experienced a ssl/tls handshake failure. The incident lasted approximately 32 minutes and affected 4385 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 04:59 | Monitoring alert triggered |
| 05:01 | On-call engineer paged |
| 05:04 | Initial investigation started |
| 05:09 | Root cause identified |
| 05:18 | Mitigation applied |
| 05:24 | Service recovery observed |
| 05:31 | Incident resolved |

## Root Cause


The incident was caused by ssl/tls handshake failure in the order-service service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 74% of requests affected
- Error rate spike: 23% (baseline: <1%)
- Latency increase: p99 went from 191ms to 2855ms


### Affected Services
- order-service
- notification-service
- billing-api

### Customer Impact

- 3266 customer-facing errors
- 21 support tickets created
- Estimated revenue impact: $3522


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 4 minutes of incident start
- On-call response was quick (3 minutes)
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
| P1 | Implement monitoring for ssl/tls handshake failure | Infrastructure | 2025-11-14 |
| P2 | Update runbook | DevOps | 2025-11-21 |
| P2 | Add load test scenario | Backend Team | 2025-11-28 |
| P3 | Review similar services | Database Team | 2025-12-07 |


## Related Incidents


- [[2025-11-07-previous-incident|Previous network incident]]
- [[runbook-order-service|order-service Runbook]]
- [[architecture-network|Network Architecture]]


---
*RCA prepared by SRE on 2025-11-11*
