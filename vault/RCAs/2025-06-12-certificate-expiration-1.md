---
title: "2025-06-12 - Certificate Expiration in billing-api"
date: 2025-06-12
severity: P1
services: [billing-api, recommendation-engine, search-api]
tags: [rca, p1, infrastructure]
status: resolved
duration_minutes: 58
author: SRE
---

# 2025-06-12 - Certificate Expiration in billing-api

## Summary

On 2025-06-12, the billing-api service experienced an infrastructure failure affecting Azure Functions. The incident lasted approximately 58 minutes and affected 6746 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 16:41 | Monitoring alert triggered |
| 16:43 | On-call engineer paged |
| 16:46 | Initial investigation started |
| 16:51 | Root cause identified |
| 17:15 | Mitigation applied |
| 17:27 | Service recovery observed |
| 17:39 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in Azure Functions. During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-billing-api-prod
- Region: eastus


## Impact


- Service degradation: 96% of requests affected
- Error rate spike: 18% (baseline: <1%)
- Latency increase: p99 went from 283ms to 5312ms


### Affected Services
- billing-api
- recommendation-engine
- search-api

### Customer Impact

- 3898 customer-facing errors
- 52 support tickets created
- Estimated revenue impact: $27820


## Resolution


1. Reverted the configuration change in Azure Functions
2. Implemented infrastructure-as-code for all changes
3. Updated deployment checklist
4. Added configuration validation in CI/CD pipeline


## Lessons Learned

### What Went Well

- Alert fired within 2 minutes of incident start
- On-call response was quick (4 minutes)
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
| P1 | Implement monitoring for certificate expiration | SRE | 2025-06-19 |
| P2 | Update runbook | Backend Team | 2025-06-26 |
| P2 | Add load test scenario | Infrastructure | 2025-07-03 |
| P3 | Review similar services | Platform Engineering | 2025-07-12 |


## Related Incidents


- [[2025-06-12-previous-incident|Previous infrastructure incident]]
- [[runbook-billing-api|billing-api Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by SRE on 2025-06-14*
