---
title: "2025-05-12 - Certificate Expiration in payment-gateway"
date: 2025-05-12
severity: P1
services: [payment-gateway, notification-service, inventory-api]
tags: [rca, p1, infrastructure]
status: resolved
duration_minutes: 99
author: SRE
---

# 2025-05-12 - Certificate Expiration in payment-gateway

## Summary

On 2025-05-12, the payment-gateway service experienced an infrastructure failure affecting Azure Event Hub. The incident lasted approximately 99 minutes and affected 9121 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 19:31 | Monitoring alert triggered |
| 19:33 | On-call engineer paged |
| 19:36 | Initial investigation started |
| 19:41 | Root cause identified |
| 20:30 | Mitigation applied |
| 20:50 | Service recovery observed |
| 21:10 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in Azure Event Hub. During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-payment-gateway-prod
- Region: eastus


## Impact


- Service degradation: 51% of requests affected
- Error rate spike: 49% (baseline: <1%)
- Latency increase: p99 went from 327ms to 3862ms


### Affected Services
- payment-gateway
- notification-service
- inventory-api

### Customer Impact

- 117 customer-facing errors
- 95 support tickets created
- Estimated revenue impact: $46613


## Resolution


1. Reverted the configuration change in Azure Event Hub
2. Implemented infrastructure-as-code for all changes
3. Updated deployment checklist
4. Added configuration validation in CI/CD pipeline


## Lessons Learned

### What Went Well

- Alert fired within 3 minutes of incident start
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
| P1 | Implement monitoring for certificate expiration | Platform Engineering | 2025-05-19 |
| P2 | Update runbook | Platform Engineering | 2025-05-26 |
| P2 | Add load test scenario | DevOps | 2025-06-02 |
| P3 | Review similar services | Backend Team | 2025-06-11 |


## Related Incidents


- [[2025-05-12-previous-incident|Previous infrastructure incident]]
- [[runbook-payment-gateway|payment-gateway Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by SRE on 2025-05-14*
