---
title: "2025-11-13 - Disk Space Exhaustion in search-api"
date: 2025-11-13
severity: P1
services: [search-api, user-service]
tags: [rca, p1, infrastructure]
status: resolved
duration_minutes: 122
author: Platform Engineering
---

# 2025-11-13 - Disk Space Exhaustion in search-api

## Summary

On 2025-11-13, the search-api service experienced an infrastructure failure affecting Application Gateway. The incident lasted approximately 122 minutes and affected 1210 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 16:39 | Monitoring alert triggered |
| 16:41 | On-call engineer paged |
| 16:44 | Initial investigation started |
| 16:49 | Root cause identified |
| 17:52 | Mitigation applied |
| 18:16 | Service recovery observed |
| 18:41 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in Application Gateway. During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-search-api-prod
- Region: eastus


## Impact


- Service degradation: 62% of requests affected
- Error rate spike: 16% (baseline: <1%)
- Latency increase: p99 went from 451ms to 5061ms


### Affected Services
- search-api
- user-service

### Customer Impact

- 1152 customer-facing errors
- 91 support tickets created
- Estimated revenue impact: $25094


## Resolution


1. Reverted the configuration change in Application Gateway
2. Implemented infrastructure-as-code for all changes
3. Updated deployment checklist
4. Added configuration validation in CI/CD pipeline


## Lessons Learned

### What Went Well

- Alert fired within 2 minutes of incident start
- On-call response was quick (5 minutes)
- Cross-team collaboration was effective
- Communication to stakeholders was timely


### What Could Be Improved  

- Need better runbooks for infrastructure issues
- Monitoring coverage gaps identified
- Load testing should cover this scenario
- Need automated rollback for faster recovery


## Action Items


| Priority | Action | Owner | Due Date |
|----------|--------|-------|----------|
| P1 | Implement monitoring for disk space exhaustion | Infrastructure | 2025-11-20 |
| P2 | Update runbook | Infrastructure | 2025-11-27 |
| P2 | Add load test scenario | Infrastructure | 2025-12-04 |
| P3 | Review similar services | Database Team | 2025-12-13 |


## Related Incidents


- [[2025-11-13-previous-incident|Previous infrastructure incident]]
- [[runbook-search-api|search-api Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by Platform Engineering on 2025-11-15*
