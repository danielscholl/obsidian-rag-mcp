---
title: "2025-12-22 - SSL/TLS Handshake Failure in order-service"
date: 2025-12-22
severity: P2
services: [order-service, payment-gateway, inventory-api]
tags: [rca, p2, network]
status: resolved
duration_minutes: 171
author: DevOps
---

# 2025-12-22 - SSL/TLS Handshake Failure in order-service

## Summary

On 2025-12-22, the order-service service experienced a ssl/tls handshake failure. The incident lasted approximately 171 minutes and affected 3568 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 07:05 | Monitoring alert triggered |
| 07:07 | On-call engineer paged |
| 07:10 | Initial investigation started |
| 07:15 | Root cause identified |
| 08:47 | Mitigation applied |
| 09:21 | Service recovery observed |
| 09:56 | Incident resolved |

## Root Cause


The incident was caused by ssl/tls handshake failure in the order-service service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 52% of requests affected
- Error rate spike: 18% (baseline: <1%)
- Latency increase: p99 went from 304ms to 7069ms


### Affected Services
- order-service
- payment-gateway
- inventory-api

### Customer Impact

- 1737 customer-facing errors
- 94 support tickets created
- Estimated revenue impact: $35780


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 4 minutes of incident start
- On-call response was quick (7 minutes)
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
| P1 | Implement monitoring for ssl/tls handshake failure | Platform Engineering | 2025-12-29 |
| P2 | Update runbook | DevOps | 2026-01-05 |
| P2 | Add load test scenario | Infrastructure | 2026-01-12 |
| P3 | Review similar services | Database Team | 2026-01-21 |


## Related Incidents


- [[2025-12-22-previous-incident|Previous network incident]]
- [[runbook-order-service|order-service Runbook]]
- [[architecture-network|Network Architecture]]


---
*RCA prepared by DevOps on 2025-12-26*
