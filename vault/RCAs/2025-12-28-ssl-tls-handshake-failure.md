---
title: "2025-12-28 - SSL/TLS Handshake Failure in recommendation-engine"
date: 2025-12-28
severity: P2
services: [search-api, user-service, recommendation-engine]
tags: [rca, p2, network]
status: resolved
duration_minutes: 94
author: SRE
---

# 2025-12-28 - SSL/TLS Handshake Failure in recommendation-engine

## Summary

On 2025-12-28, the recommendation-engine service experienced a ssl/tls handshake failure. The incident lasted approximately 94 minutes and affected 9711 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 07:05 | Monitoring alert triggered |
| 07:07 | On-call engineer paged |
| 07:10 | Initial investigation started |
| 07:15 | Root cause identified |
| 08:01 | Mitigation applied |
| 08:20 | Service recovery observed |
| 08:39 | Incident resolved |

## Root Cause


The incident was caused by ssl/tls handshake failure in the recommendation-engine service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 67% of requests affected
- Error rate spike: 44% (baseline: <1%)
- Latency increase: p99 went from 461ms to 9136ms


### Affected Services
- search-api
- user-service
- recommendation-engine

### Customer Impact

- 3219 customer-facing errors
- 39 support tickets created
- Estimated revenue impact: $15902


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 1 minutes of incident start
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
| P1 | Implement monitoring for ssl/tls handshake failure | Backend Team | 2026-01-04 |
| P2 | Update runbook | DevOps | 2026-01-11 |
| P2 | Add load test scenario | Backend Team | 2026-01-18 |
| P3 | Review similar services | Platform Engineering | 2026-01-27 |


## Related Incidents


- [[2025-12-28-previous-incident|Previous network incident]]
- [[runbook-recommendation-engine|recommendation-engine Runbook]]
- [[architecture-network|Network Architecture]]


---
*RCA prepared by SRE on 2025-12-29*
