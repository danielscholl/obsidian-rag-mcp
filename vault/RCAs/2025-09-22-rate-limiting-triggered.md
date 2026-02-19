---
title: "2025-09-22 - Rate Limiting Triggered in inventory-api"
date: 2025-09-22
severity: P3
services: [inventory-api, payment-gateway, search-api]
tags: [rca, p3, application]
status: resolved
duration_minutes: 151
author: SRE
---

# 2025-09-22 - Rate Limiting Triggered in inventory-api

## Summary

On 2025-09-22, the inventory-api service experienced a rate limiting triggered. The incident lasted approximately 151 minutes and affected 7450 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 01:33 | Monitoring alert triggered |
| 01:35 | On-call engineer paged |
| 01:38 | Initial investigation started |
| 01:43 | Root cause identified |
| 03:03 | Mitigation applied |
| 03:33 | Service recovery observed |
| 04:04 | Incident resolved |

## Root Cause


The incident was caused by rate limiting triggered in the inventory-api service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection


## Impact


- Service degradation: 85% of requests affected
- Error rate spike: 25% (baseline: <1%)
- Latency increase: p99 went from 184ms to 3092ms


### Affected Services
- inventory-api
- payment-gateway
- search-api

### Customer Impact

- 4894 customer-facing errors
- 35 support tickets created
- Estimated revenue impact: $29188


## Resolution


1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps


## Lessons Learned

### What Went Well

- Alert fired within 2 minutes of incident start
- On-call response was quick (5 minutes)
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
| P1 | Implement monitoring for rate limiting triggered | Platform Engineering | 2025-09-29 |
| P2 | Update runbook | DevOps | 2025-10-06 |
| P2 | Add load test scenario | Platform Engineering | 2025-10-13 |
| P3 | Review similar services | Database Team | 2025-10-22 |


## Related Incidents


- [[2025-09-22-previous-incident|Previous application incident]]
- [[runbook-inventory-api|inventory-api Runbook]]
- [[architecture-application|Application Architecture]]


---
*RCA prepared by SRE on 2025-09-24*
