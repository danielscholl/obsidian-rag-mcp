---
title: "2025-11-20 - Load Balancer Misconfiguration in inventory-api"
date: 2025-11-20
severity: P2
services: [inventory-api, recommendation-engine, order-service]
tags: [rca, p2, infrastructure]
status: resolved
duration_minutes: 161
author: DevOps
---

# 2025-11-20 - Load Balancer Misconfiguration in inventory-api

## Summary

On 2025-11-20, the inventory-api service experienced an infrastructure failure affecting Azure Storage. The incident lasted approximately 161 minutes and affected 1457 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 20:42 | Monitoring alert triggered |
| 20:44 | On-call engineer paged |
| 20:47 | Initial investigation started |
| 20:52 | Root cause identified |
| 22:18 | Mitigation applied |
| 22:50 | Service recovery observed |
| 23:23 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in Azure Storage. During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-inventory-api-prod
- Region: westus2


## Impact


- Service degradation: 92% of requests affected
- Error rate spike: 40% (baseline: <1%)
- Latency increase: p99 went from 139ms to 8656ms


### Affected Services
- inventory-api
- recommendation-engine
- order-service

### Customer Impact

- 2102 customer-facing errors
- 36 support tickets created
- Estimated revenue impact: $36172


## Resolution


1. Reverted the configuration change in Azure Storage
2. Implemented infrastructure-as-code for all changes
3. Updated deployment checklist
4. Added configuration validation in CI/CD pipeline


## Lessons Learned

### What Went Well

- Alert fired within 3 minutes of incident start
- On-call response was quick (8 minutes)
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
| P1 | Implement monitoring for load balancer misconfiguration | Infrastructure | 2025-11-27 |
| P2 | Update runbook | Backend Team | 2025-12-04 |
| P2 | Add load test scenario | Backend Team | 2025-12-11 |
| P3 | Review similar services | Platform Engineering | 2025-12-20 |


## Related Incidents


- [[2025-11-20-previous-incident|Previous infrastructure incident]]
- [[runbook-inventory-api|inventory-api Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by DevOps on 2025-11-23*
