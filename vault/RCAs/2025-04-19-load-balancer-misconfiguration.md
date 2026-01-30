---
title: "2025-04-19 - Load Balancer Misconfiguration in billing-api"
date: 2025-04-19
severity: P2
services: [billing-api, payment-gateway]
tags: [rca, p2, infrastructure]
status: resolved
duration_minutes: 139
author: Platform Engineering
---

# 2025-04-19 - Load Balancer Misconfiguration in billing-api

## Summary

On 2025-04-19, the billing-api service experienced an infrastructure failure affecting Azure Service Bus. The incident lasted approximately 139 minutes and affected 5246 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 00:32 | Monitoring alert triggered |
| 00:34 | On-call engineer paged |
| 00:37 | Initial investigation started |
| 00:42 | Root cause identified |
| 01:55 | Mitigation applied |
| 02:23 | Service recovery observed |
| 02:51 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in Azure Service Bus. During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-billing-api-prod
- Region: eastus


## Impact


- Service degradation: 68% of requests affected
- Error rate spike: 10% (baseline: <1%)
- Latency increase: p99 went from 184ms to 7109ms


### Affected Services
- billing-api
- payment-gateway

### Customer Impact

- 3151 customer-facing errors
- 43 support tickets created
- Estimated revenue impact: $12610


## Resolution


1. Reverted the configuration change in Azure Service Bus
2. Implemented infrastructure-as-code for all changes
3. Updated deployment checklist
4. Added configuration validation in CI/CD pipeline


## Lessons Learned

### What Went Well

- Alert fired within 4 minutes of incident start
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
| P1 | Implement monitoring for load balancer misconfiguration | SRE | 2025-04-26 |
| P2 | Update runbook | Backend Team | 2025-05-03 |
| P2 | Add load test scenario | Infrastructure | 2025-05-10 |
| P3 | Review similar services | DevOps | 2025-05-19 |


## Related Incidents


- [[2025-04-19-previous-incident|Previous infrastructure incident]]
- [[runbook-billing-api|billing-api Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by Platform Engineering on 2025-04-21*
