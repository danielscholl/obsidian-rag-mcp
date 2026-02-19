---
title: "2025-05-23 - Load Balancer Misconfiguration in analytics-pipeline"
date: 2025-05-23
severity: P2
services: [analytics-pipeline, recommendation-engine, billing-api, payment-gateway]
tags: [rca, p2, infrastructure]
status: resolved
duration_minutes: 28
author: DevOps
---

# 2025-05-23 - Load Balancer Misconfiguration in analytics-pipeline

## Summary

On 2025-05-23, the analytics-pipeline service experienced an infrastructure failure affecting Azure App Service. The incident lasted approximately 28 minutes and affected 2291 users and 4 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 21:07 | Monitoring alert triggered |
| 21:09 | On-call engineer paged |
| 21:12 | Initial investigation started |
| 21:17 | Root cause identified |
| 21:23 | Mitigation applied |
| 21:29 | Service recovery observed |
| 21:35 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in Azure App Service. During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-analytics-pipeline-prod
- Region: eastus


## Impact


- Service degradation: 92% of requests affected
- Error rate spike: 13% (baseline: <1%)
- Latency increase: p99 went from 489ms to 4320ms


### Affected Services
- analytics-pipeline
- recommendation-engine
- billing-api
- payment-gateway

### Customer Impact

- 1860 customer-facing errors
- 66 support tickets created
- Estimated revenue impact: $45726


## Resolution


1. Reverted the configuration change in Azure App Service
2. Implemented infrastructure-as-code for all changes
3. Updated deployment checklist
4. Added configuration validation in CI/CD pipeline


## Lessons Learned

### What Went Well

- Alert fired within 5 minutes of incident start
- On-call response was quick (10 minutes)
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
| P1 | Implement monitoring for load balancer misconfiguration | Infrastructure | 2025-05-30 |
| P2 | Update runbook | SRE | 2025-06-06 |
| P2 | Add load test scenario | DevOps | 2025-06-13 |
| P3 | Review similar services | Infrastructure | 2025-06-22 |


## Related Incidents


- [[2025-05-23-previous-incident|Previous infrastructure incident]]
- [[runbook-analytics-pipeline|analytics-pipeline Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by DevOps on 2025-05-27*
