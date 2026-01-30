---
title: "2025-08-13 - Load Balancer Misconfiguration in inventory-api"
date: 2025-08-13
severity: P2
services: [inventory-api, auth-service, analytics-pipeline, search-api]
tags: [rca, p2, infrastructure]
status: resolved
duration_minutes: 169
author: DevOps
---

# 2025-08-13 - Load Balancer Misconfiguration in inventory-api

## Summary

On 2025-08-13, the inventory-api service experienced an infrastructure failure affecting AKS (Kubernetes). The incident lasted approximately 169 minutes and affected 8252 users and 4 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 08:50 | Monitoring alert triggered |
| 08:52 | On-call engineer paged |
| 08:55 | Initial investigation started |
| 09:00 | Root cause identified |
| 10:31 | Mitigation applied |
| 11:05 | Service recovery observed |
| 11:39 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in AKS (Kubernetes). During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-inventory-api-prod
- Region: westus2


## Impact


- Service degradation: 97% of requests affected
- Error rate spike: 24% (baseline: <1%)
- Latency increase: p99 went from 420ms to 8434ms


### Affected Services
- inventory-api
- auth-service
- analytics-pipeline
- search-api

### Customer Impact

- 2987 customer-facing errors
- 83 support tickets created
- Estimated revenue impact: $35443


## Resolution


1. Reverted the configuration change in AKS (Kubernetes)
2. Implemented infrastructure-as-code for all changes
3. Updated deployment checklist
4. Added configuration validation in CI/CD pipeline


## Lessons Learned

### What Went Well

- Alert fired within 3 minutes of incident start
- On-call response was quick (6 minutes)
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
| P1 | Implement monitoring for load balancer misconfiguration | DevOps | 2025-08-20 |
| P2 | Update runbook | DevOps | 2025-08-27 |
| P2 | Add load test scenario | SRE | 2025-09-03 |
| P3 | Review similar services | Database Team | 2025-09-12 |


## Related Incidents


- [[2025-08-13-previous-incident|Previous infrastructure incident]]
- [[runbook-inventory-api|inventory-api Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by DevOps on 2025-08-17*
