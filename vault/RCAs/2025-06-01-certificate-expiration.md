---
title: "2025-06-01 - Certificate Expiration in search-api"
date: 2025-06-01
severity: P1
services: [search-api, recommendation-engine, notification-service]
tags: [rca, p1, infrastructure]
status: resolved
duration_minutes: 90
author: Database Team
---

# 2025-06-01 - Certificate Expiration in search-api

## Summary

On 2025-06-01, the search-api service experienced an infrastructure failure affecting Azure App Service. The incident lasted approximately 90 minutes and affected 2282 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 23:09 | Monitoring alert triggered |
| 23:11 | On-call engineer paged |
| 23:14 | Initial investigation started |
| 23:19 | Root cause identified |
| 00:03 | Mitigation applied |
| 00:21 | Service recovery observed |
| 00:39 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in Azure App Service. During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-search-api-prod
- Region: westus2


## Impact


- Service degradation: 65% of requests affected
- Error rate spike: 36% (baseline: <1%)
- Latency increase: p99 went from 234ms to 4211ms


### Affected Services
- search-api
- recommendation-engine
- notification-service

### Customer Impact

- 1958 customer-facing errors
- 19 support tickets created
- Estimated revenue impact: $7565


## Resolution


1. Reverted the configuration change in Azure App Service
2. Implemented infrastructure-as-code for all changes
3. Updated deployment checklist
4. Added configuration validation in CI/CD pipeline


## Lessons Learned

### What Went Well

- Alert fired within 4 minutes of incident start
- On-call response was quick (2 minutes)
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
| P1 | Implement monitoring for certificate expiration | Backend Team | 2025-06-08 |
| P2 | Update runbook | Infrastructure | 2025-06-15 |
| P2 | Add load test scenario | Infrastructure | 2025-06-22 |
| P3 | Review similar services | Backend Team | 2025-07-01 |


## Related Incidents


- [[2025-06-01-previous-incident|Previous infrastructure incident]]
- [[runbook-search-api|search-api Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by Database Team on 2025-06-06*
