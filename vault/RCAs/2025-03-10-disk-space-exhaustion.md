---
title: "2025-03-10 - Disk Space Exhaustion in inventory-api"
date: 2025-03-10
severity: P1
services: [inventory-api, auth-service, analytics-pipeline]
tags: [rca, p1, infrastructure]
status: resolved
duration_minutes: 35
author: Infrastructure
---

# 2025-03-10 - Disk Space Exhaustion in inventory-api

## Summary

On 2025-03-10, the inventory-api service experienced an infrastructure failure affecting AKS (Kubernetes). The incident lasted approximately 35 minutes and affected 7672 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 07:58 | Monitoring alert triggered |
| 08:00 | On-call engineer paged |
| 08:03 | Initial investigation started |
| 08:08 | Root cause identified |
| 08:19 | Mitigation applied |
| 08:26 | Service recovery observed |
| 08:33 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in AKS (Kubernetes). During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-inventory-api-prod
- Region: eastus


## Impact


- Service degradation: 70% of requests affected
- Error rate spike: 23% (baseline: <1%)
- Latency increase: p99 went from 156ms to 7940ms


### Affected Services
- inventory-api
- auth-service
- analytics-pipeline

### Customer Impact

- 1696 customer-facing errors
- 28 support tickets created
- Estimated revenue impact: $37201


## Resolution


1. Reverted the configuration change in AKS (Kubernetes)
2. Implemented infrastructure-as-code for all changes
3. Updated deployment checklist
4. Added configuration validation in CI/CD pipeline


## Lessons Learned

### What Went Well

- Alert fired within 3 minutes of incident start
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
| P1 | Implement monitoring for disk space exhaustion | Backend Team | 2025-03-17 |
| P2 | Update runbook | Database Team | 2025-03-24 |
| P2 | Add load test scenario | Backend Team | 2025-03-31 |
| P3 | Review similar services | Backend Team | 2025-04-09 |


## Related Incidents


- [[2025-03-10-previous-incident|Previous infrastructure incident]]
- [[runbook-inventory-api|inventory-api Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by Infrastructure on 2025-03-14*
