---
title: "2025-02-17 - Deployment Rollback Required in search-api"
date: 2025-02-17
severity: P2
services: [search-api, user-service, recommendation-engine]
tags: [rca, p2, deployment]
status: resolved
duration_minutes: 67
author: Infrastructure
---

# 2025-02-17 - Deployment Rollback Required in search-api

## Summary

On 2025-02-17, the search-api service experienced a deployment rollback required. The incident lasted approximately 67 minutes and affected 1864 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 02:17 | Monitoring alert triggered |
| 02:19 | On-call engineer paged |
| 02:22 | Initial investigation started |
| 02:27 | Root cause identified |
| 02:57 | Mitigation applied |
| 03:10 | Service recovery observed |
| 03:24 | Incident resolved |

## Root Cause


The incident was caused by deployment rollback required in the search-api service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 57% of requests affected
- Error rate spike: 45% (baseline: <1%)
- Latency increase: p99 went from 293ms to 8767ms


### Affected Services
- search-api
- user-service
- recommendation-engine

### Customer Impact

- 1858 customer-facing errors
- 18 support tickets created
- Estimated revenue impact: $9979


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 5 minutes of incident start
- On-call response was quick (5 minutes)
- Cross-team collaboration was effective
- Communication to stakeholders was timely


### What Could Be Improved  

- Need better runbooks for deployment issues
- Monitoring coverage gaps identified
- Load testing should cover this scenario
- Need automated rollback for faster recovery


## Action Items


| Priority | Action | Owner | Due Date |
|----------|--------|-------|----------|
| P1 | Implement monitoring for deployment rollback required | Platform Engineering | 2025-02-24 |
| P2 | Update runbook | Database Team | 2025-03-03 |
| P2 | Add load test scenario | DevOps | 2025-03-10 |
| P3 | Review similar services | SRE | 2025-03-19 |


## Related Incidents


- [[2025-02-17-previous-incident|Previous deployment incident]]
- [[runbook-search-api|search-api Runbook]]
- [[architecture-deployment|Deployment Architecture]]


---
*RCA prepared by Infrastructure on 2025-02-22*
