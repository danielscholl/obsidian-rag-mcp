---
title: "2025-03-29 - Certificate Expiration in billing-api"
date: 2025-03-29
severity: P1
services: [billing-api, user-service]
tags: [rca, p1, infrastructure]
status: resolved
duration_minutes: 168
author: SRE
---

# 2025-03-29 - Certificate Expiration in billing-api

## Summary

On 2025-03-29, the billing-api service experienced an infrastructure failure affecting Azure Functions. The incident lasted approximately 168 minutes and affected 5483 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 06:37 | Monitoring alert triggered |
| 06:39 | On-call engineer paged |
| 06:42 | Initial investigation started |
| 06:47 | Root cause identified |
| 08:17 | Mitigation applied |
| 08:51 | Service recovery observed |
| 09:25 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in Azure Functions. During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-billing-api-prod
- Region: westeurope


## Impact


- Service degradation: 64% of requests affected
- Error rate spike: 32% (baseline: <1%)
- Latency increase: p99 went from 332ms to 2429ms


### Affected Services
- billing-api
- user-service

### Customer Impact

- 476 customer-facing errors
- 16 support tickets created
- Estimated revenue impact: $35960


## Resolution


1. Reverted the configuration change in Azure Functions
2. Implemented infrastructure-as-code for all changes
3. Updated deployment checklist
4. Added configuration validation in CI/CD pipeline


## Lessons Learned

### What Went Well

- Alert fired within 1 minutes of incident start
- On-call response was quick (9 minutes)
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
| P1 | Implement monitoring for certificate expiration | Platform Engineering | 2025-04-05 |
| P2 | Update runbook | SRE | 2025-04-12 |
| P2 | Add load test scenario | Platform Engineering | 2025-04-19 |
| P3 | Review similar services | Backend Team | 2025-04-28 |


## Related Incidents


- [[2025-03-29-previous-incident|Previous infrastructure incident]]
- [[runbook-billing-api|billing-api Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by SRE on 2025-03-30*
