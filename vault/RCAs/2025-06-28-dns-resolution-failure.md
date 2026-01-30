---
title: "2025-06-28 - DNS Resolution Failure in recommendation-engine"
date: 2025-06-28
severity: P1
services: [recommendation-engine, inventory-api]
tags: [rca, p1, network]
status: resolved
duration_minutes: 88
author: Backend Team
---

# 2025-06-28 - DNS Resolution Failure in recommendation-engine

## Summary

On 2025-06-28, the recommendation-engine service experienced a dns resolution failure. The incident lasted approximately 88 minutes and affected 1938 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 15:06 | Monitoring alert triggered |
| 15:08 | On-call engineer paged |
| 15:11 | Initial investigation started |
| 15:16 | Root cause identified |
| 15:58 | Mitigation applied |
| 16:16 | Service recovery observed |
| 16:34 | Incident resolved |

## Root Cause


The incident was caused by dns resolution failure in the recommendation-engine service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 77% of requests affected
- Error rate spike: 34% (baseline: <1%)
- Latency increase: p99 went from 256ms to 6822ms


### Affected Services
- recommendation-engine
- inventory-api

### Customer Impact

- 2372 customer-facing errors
- 88 support tickets created
- Estimated revenue impact: $1989


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
| P1 | Implement monitoring for dns resolution failure | DevOps | 2025-07-05 |
| P2 | Update runbook | Database Team | 2025-07-12 |
| P2 | Add load test scenario | Infrastructure | 2025-07-19 |
| P3 | Review similar services | SRE | 2025-07-28 |


## Related Incidents


- [[2025-06-28-previous-incident|Previous network incident]]
- [[runbook-recommendation-engine|recommendation-engine Runbook]]
- [[architecture-network|Network Architecture]]


---
*RCA prepared by Backend Team on 2025-07-02*
