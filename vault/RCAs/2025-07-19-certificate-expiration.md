---
title: "2025-07-19 - Certificate Expiration in billing-api"
date: 2025-07-19
severity: P1
services: [billing-api, recommendation-engine, search-api]
tags: [rca, p1, infrastructure]
status: resolved
duration_minutes: 170
author: SRE
---

# 2025-07-19 - Certificate Expiration in billing-api

## Summary

On 2025-07-19, the billing-api service experienced an infrastructure failure affecting Azure Functions. The incident lasted approximately 170 minutes and affected 7320 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 10:34 | Monitoring alert triggered |
| 10:36 | On-call engineer paged |
| 10:39 | Initial investigation started |
| 10:44 | Root cause identified |
| 12:16 | Mitigation applied |
| 12:50 | Service recovery observed |
| 13:24 | Incident resolved |

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


- Service degradation: 81% of requests affected
- Error rate spike: 26% (baseline: <1%)
- Latency increase: p99 went from 282ms to 9502ms


### Affected Services
- billing-api
- recommendation-engine
- search-api

### Customer Impact

- 2025 customer-facing errors
- 65 support tickets created
- Estimated revenue impact: $13711


## Resolution


1. Reverted the configuration change in Azure Functions
2. Implemented infrastructure-as-code for all changes
3. Updated deployment checklist
4. Added configuration validation in CI/CD pipeline


## Lessons Learned

### What Went Well

- Alert fired within 1 minutes of incident start
- On-call response was quick (5 minutes)
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
| P1 | Implement monitoring for certificate expiration | SRE | 2025-07-26 |
| P2 | Update runbook | DevOps | 2025-08-02 |
| P2 | Add load test scenario | DevOps | 2025-08-09 |
| P3 | Review similar services | Backend Team | 2025-08-18 |


## Related Incidents


- [[2025-07-19-previous-incident|Previous infrastructure incident]]
- [[runbook-billing-api|billing-api Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by SRE on 2025-07-21*
