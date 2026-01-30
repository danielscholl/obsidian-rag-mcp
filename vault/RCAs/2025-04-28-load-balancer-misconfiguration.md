---
title: "2025-04-28 - Load Balancer Misconfiguration in analytics-pipeline"
date: 2025-04-28
severity: P2
services: [analytics-pipeline, recommendation-engine]
tags: [rca, p2, infrastructure]
status: resolved
duration_minutes: 26
author: SRE
---

# 2025-04-28 - Load Balancer Misconfiguration in analytics-pipeline

## Summary

On 2025-04-28, the analytics-pipeline service experienced an infrastructure failure affecting AKS (Kubernetes). The incident lasted approximately 26 minutes and affected 1987 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 17:07 | Monitoring alert triggered |
| 17:09 | On-call engineer paged |
| 17:12 | Initial investigation started |
| 17:17 | Root cause identified |
| 17:22 | Mitigation applied |
| 17:27 | Service recovery observed |
| 17:33 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in AKS (Kubernetes). During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-analytics-pipeline-prod
- Region: westeurope


## Impact


- Service degradation: 56% of requests affected
- Error rate spike: 10% (baseline: <1%)
- Latency increase: p99 went from 494ms to 7203ms


### Affected Services
- analytics-pipeline
- recommendation-engine

### Customer Impact

- 4698 customer-facing errors
- 81 support tickets created
- Estimated revenue impact: $10177


## Resolution


1. Reverted the configuration change in AKS (Kubernetes)
2. Implemented infrastructure-as-code for all changes
3. Updated deployment checklist
4. Added configuration validation in CI/CD pipeline


## Lessons Learned

### What Went Well

- Alert fired within 1 minutes of incident start
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
| P1 | Implement monitoring for load balancer misconfiguration | DevOps | 2025-05-05 |
| P2 | Update runbook | SRE | 2025-05-12 |
| P2 | Add load test scenario | Infrastructure | 2025-05-19 |
| P3 | Review similar services | DevOps | 2025-05-28 |


## Related Incidents


- [[2025-04-28-previous-incident|Previous infrastructure incident]]
- [[runbook-analytics-pipeline|analytics-pipeline Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by SRE on 2025-05-03*
