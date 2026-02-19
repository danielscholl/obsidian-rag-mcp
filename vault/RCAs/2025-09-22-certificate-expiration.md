---
title: "2025-09-22 - Certificate Expiration in payment-gateway"
date: 2025-09-22
severity: P1
services: [payment-gateway, order-service]
tags: [rca, p1, infrastructure]
status: resolved
duration_minutes: 124
author: Backend Team
---

# 2025-09-22 - Certificate Expiration in payment-gateway

## Summary

On 2025-09-22, the payment-gateway service experienced an infrastructure failure affecting Azure CDN. The incident lasted approximately 124 minutes and affected 4283 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 05:02 | Monitoring alert triggered |
| 05:04 | On-call engineer paged |
| 05:07 | Initial investigation started |
| 05:12 | Root cause identified |
| 06:16 | Mitigation applied |
| 06:41 | Service recovery observed |
| 07:06 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in Azure CDN. During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-payment-gateway-prod
- Region: westeurope


## Impact


- Service degradation: 70% of requests affected
- Error rate spike: 34% (baseline: <1%)
- Latency increase: p99 went from 471ms to 5390ms


### Affected Services
- payment-gateway
- order-service

### Customer Impact

- 3538 customer-facing errors
- 96 support tickets created
- Estimated revenue impact: $7094


## Resolution


1. Reverted the configuration change in Azure CDN
2. Implemented infrastructure-as-code for all changes
3. Updated deployment checklist
4. Added configuration validation in CI/CD pipeline


## Lessons Learned

### What Went Well

- Alert fired within 4 minutes of incident start
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
| P1 | Implement monitoring for certificate expiration | Database Team | 2025-09-29 |
| P2 | Update runbook | SRE | 2025-10-06 |
| P2 | Add load test scenario | Backend Team | 2025-10-13 |
| P3 | Review similar services | Infrastructure | 2025-10-22 |


## Related Incidents


- [[2025-09-22-previous-incident|Previous infrastructure incident]]
- [[runbook-payment-gateway|payment-gateway Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by Backend Team on 2025-09-26*
