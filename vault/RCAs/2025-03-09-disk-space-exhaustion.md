---
title: "2025-03-09 - Disk Space Exhaustion in inventory-api"
date: 2025-03-09
severity: P1
services: [inventory-api, search-api, notification-service, order-service]
tags: [rca, p1, infrastructure]
status: resolved
duration_minutes: 28
author: Database Team
---

# 2025-03-09 - Disk Space Exhaustion in inventory-api

## Summary

On 2025-03-09, the inventory-api service experienced an infrastructure failure affecting Azure App Service. The incident lasted approximately 28 minutes and affected 4242 users and 4 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 05:27 | Monitoring alert triggered |
| 05:29 | On-call engineer paged |
| 05:32 | Initial investigation started |
| 05:37 | Root cause identified |
| 05:43 | Mitigation applied |
| 05:49 | Service recovery observed |
| 05:55 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in Azure App Service. During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-inventory-api-prod
- Region: eastus


## Impact


- Service degradation: 50% of requests affected
- Error rate spike: 22% (baseline: <1%)
- Latency increase: p99 went from 131ms to 8463ms


### Affected Services
- inventory-api
- search-api
- notification-service
- order-service

### Customer Impact

- 2014 customer-facing errors
- 44 support tickets created
- Estimated revenue impact: $2030


## Resolution


1. Reverted the configuration change in Azure App Service
2. Implemented infrastructure-as-code for all changes
3. Updated deployment checklist
4. Added configuration validation in CI/CD pipeline


## Lessons Learned

### What Went Well

- Alert fired within 1 minutes of incident start
- On-call response was quick (3 minutes)
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
| P1 | Implement monitoring for disk space exhaustion | Platform Engineering | 2025-03-16 |
| P2 | Update runbook | Platform Engineering | 2025-03-23 |
| P2 | Add load test scenario | Infrastructure | 2025-03-30 |
| P3 | Review similar services | Infrastructure | 2025-04-08 |


## Related Incidents


- [[2025-03-09-previous-incident|Previous infrastructure incident]]
- [[runbook-inventory-api|inventory-api Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by Database Team on 2025-03-14*
