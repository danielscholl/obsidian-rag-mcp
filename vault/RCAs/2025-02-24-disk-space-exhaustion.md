---
title: "2025-02-24 - Disk Space Exhaustion in billing-api"
date: 2025-02-24
severity: P1
services: [billing-api, order-service]
tags: [rca, p1, infrastructure]
status: resolved
duration_minutes: 166
author: Infrastructure
---

# 2025-02-24 - Disk Space Exhaustion in billing-api

## Summary

On 2025-02-24, the billing-api service experienced an infrastructure failure affecting AKS (Kubernetes). The incident lasted approximately 166 minutes and affected 7785 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 07:16 | Monitoring alert triggered |
| 07:18 | On-call engineer paged |
| 07:21 | Initial investigation started |
| 07:26 | Root cause identified |
| 08:55 | Mitigation applied |
| 09:28 | Service recovery observed |
| 10:02 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in AKS (Kubernetes). During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-billing-api-prod
- Region: eastus


## Impact


- Service degradation: 86% of requests affected
- Error rate spike: 41% (baseline: <1%)
- Latency increase: p99 went from 195ms to 6854ms


### Affected Services
- billing-api
- order-service

### Customer Impact

- 4599 customer-facing errors
- 49 support tickets created
- Estimated revenue impact: $18667


## Resolution


1. Reverted the configuration change in AKS (Kubernetes)
2. Implemented infrastructure-as-code for all changes
3. Updated deployment checklist
4. Added configuration validation in CI/CD pipeline


## Lessons Learned

### What Went Well

- Alert fired within 5 minutes of incident start
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
| P1 | Implement monitoring for disk space exhaustion | Platform Engineering | 2025-03-03 |
| P2 | Update runbook | Infrastructure | 2025-03-10 |
| P2 | Add load test scenario | Platform Engineering | 2025-03-17 |
| P3 | Review similar services | Infrastructure | 2025-03-26 |


## Related Incidents


- [[2025-02-24-previous-incident|Previous infrastructure incident]]
- [[runbook-billing-api|billing-api Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by Infrastructure on 2025-02-26*
