---
title: "2025-10-03 - SSL/TLS Handshake Failure in auth-service"
date: 2025-10-03
severity: P2
services: [auth-service, recommendation-engine]
tags: [rca, p2, network]
status: resolved
duration_minutes: 137
author: Database Team
---

# 2025-10-03 - SSL/TLS Handshake Failure in auth-service

## Summary

On 2025-10-03, the auth-service service experienced a ssl/tls handshake failure. The incident lasted approximately 137 minutes and affected 9002 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 02:57 | Monitoring alert triggered |
| 02:59 | On-call engineer paged |
| 03:02 | Initial investigation started |
| 03:07 | Root cause identified |
| 04:19 | Mitigation applied |
| 04:46 | Service recovery observed |
| 05:14 | Incident resolved |

## Root Cause


The incident was caused by ssl/tls handshake failure in the auth-service service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 72% of requests affected
- Error rate spike: 16% (baseline: <1%)
- Latency increase: p99 went from 366ms to 9994ms


### Affected Services
- auth-service
- recommendation-engine

### Customer Impact

- 4034 customer-facing errors
- 22 support tickets created
- Estimated revenue impact: $28145


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 4 minutes of incident start
- On-call response was quick (8 minutes)
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
| P1 | Implement monitoring for ssl/tls handshake failure | Platform Engineering | 2025-10-10 |
| P2 | Update runbook | DevOps | 2025-10-17 |
| P2 | Add load test scenario | Platform Engineering | 2025-10-24 |
| P3 | Review similar services | Platform Engineering | 2025-11-02 |


## Related Incidents


- [[2025-10-03-previous-incident|Previous network incident]]
- [[runbook-auth-service|auth-service Runbook]]
- [[architecture-network|Network Architecture]]


---
*RCA prepared by Database Team on 2025-10-04*
