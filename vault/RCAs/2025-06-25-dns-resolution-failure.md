---
title: "2025-06-25 - DNS Resolution Failure in recommendation-engine"
date: 2025-06-25
severity: P1
services: [recommendation-engine, search-api]
tags: [rca, p1, network]
status: resolved
duration_minutes: 82
author: Infrastructure
---

# 2025-06-25 - DNS Resolution Failure in recommendation-engine

## Summary

On 2025-06-25, the recommendation-engine service experienced a dns resolution failure. The incident lasted approximately 82 minutes and affected 9737 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 18:27 | Monitoring alert triggered |
| 18:29 | On-call engineer paged |
| 18:32 | Initial investigation started |
| 18:37 | Root cause identified |
| 19:16 | Mitigation applied |
| 19:32 | Service recovery observed |
| 19:49 | Incident resolved |

## Root Cause


The incident was caused by dns resolution failure in the recommendation-engine service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 58% of requests affected
- Error rate spike: 12% (baseline: <1%)
- Latency increase: p99 went from 292ms to 8721ms


### Affected Services
- recommendation-engine
- search-api

### Customer Impact

- 2595 customer-facing errors
- 28 support tickets created
- Estimated revenue impact: $34335


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
| P1 | Implement monitoring for dns resolution failure | Database Team | 2025-07-02 |
| P2 | Update runbook | Platform Engineering | 2025-07-09 |
| P2 | Add load test scenario | Database Team | 2025-07-16 |
| P3 | Review similar services | Database Team | 2025-07-25 |


## Related Incidents


- [[2025-06-25-previous-incident|Previous network incident]]
- [[runbook-recommendation-engine|recommendation-engine Runbook]]
- [[architecture-network|Network Architecture]]


---
*RCA prepared by Infrastructure on 2025-06-27*
