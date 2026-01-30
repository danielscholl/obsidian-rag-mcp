---
title: "2025-12-29 - SSL/TLS Handshake Failure in payment-gateway"
date: 2025-12-29
severity: P2
services: [payment-gateway, search-api, auth-service]
tags: [rca, p2, network]
status: resolved
duration_minutes: 118
author: Infrastructure
---

# 2025-12-29 - SSL/TLS Handshake Failure in payment-gateway

## Summary

On 2025-12-29, the payment-gateway service experienced a ssl/tls handshake failure. The incident lasted approximately 118 minutes and affected 8963 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 19:36 | Monitoring alert triggered |
| 19:38 | On-call engineer paged |
| 19:41 | Initial investigation started |
| 19:46 | Root cause identified |
| 20:46 | Mitigation applied |
| 21:10 | Service recovery observed |
| 21:34 | Incident resolved |

## Root Cause


The incident was caused by ssl/tls handshake failure in the payment-gateway service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 98% of requests affected
- Error rate spike: 28% (baseline: <1%)
- Latency increase: p99 went from 298ms to 6129ms


### Affected Services
- payment-gateway
- search-api
- auth-service

### Customer Impact

- 808 customer-facing errors
- 65 support tickets created
- Estimated revenue impact: $22974


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 2 minutes of incident start
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
| P1 | Implement monitoring for ssl/tls handshake failure | Database Team | 2026-01-05 |
| P2 | Update runbook | DevOps | 2026-01-12 |
| P2 | Add load test scenario | DevOps | 2026-01-19 |
| P3 | Review similar services | Database Team | 2026-01-28 |


## Related Incidents


- [[2025-12-29-previous-incident|Previous network incident]]
- [[runbook-payment-gateway|payment-gateway Runbook]]
- [[architecture-network|Network Architecture]]


---
*RCA prepared by Infrastructure on 2026-01-03*
