---
title: "2025-06-12 - Certificate Expiration in payment-gateway"
date: 2025-06-12
severity: P1
services: [analytics-pipeline, payment-gateway]
tags: [rca, p1, infrastructure]
status: resolved
duration_minutes: 164
author: Backend Team
---

# 2025-06-12 - Certificate Expiration in payment-gateway

## Summary

On 2025-06-12, the payment-gateway service experienced an infrastructure failure affecting Azure Event Hub. The incident lasted approximately 164 minutes and affected 4927 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 06:54 | Monitoring alert triggered |
| 06:56 | On-call engineer paged |
| 06:59 | Initial investigation started |
| 07:04 | Root cause identified |
| 08:32 | Mitigation applied |
| 09:05 | Service recovery observed |
| 09:38 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in Azure Event Hub. During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-payment-gateway-prod
- Region: westus2


## Impact


- Service degradation: 72% of requests affected
- Error rate spike: 46% (baseline: <1%)
- Latency increase: p99 went from 323ms to 6789ms


### Affected Services
- analytics-pipeline
- payment-gateway

### Customer Impact

- 2987 customer-facing errors
- 100 support tickets created
- Estimated revenue impact: $11885


## Resolution


1. Reverted the configuration change in Azure Event Hub
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
| P1 | Implement monitoring for certificate expiration | Backend Team | 2025-06-19 |
| P2 | Update runbook | DevOps | 2025-06-26 |
| P2 | Add load test scenario | Infrastructure | 2025-07-03 |
| P3 | Review similar services | DevOps | 2025-07-12 |


## Related Incidents


- [[2025-06-12-previous-incident|Previous infrastructure incident]]
- [[runbook-payment-gateway|payment-gateway Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by Backend Team on 2025-06-15*
