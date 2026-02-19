---
title: "2025-01-30 - Disk Space Exhaustion in payment-gateway"
date: 2025-01-30
severity: P1
services: [payment-gateway, auth-service]
tags: [rca, p1, infrastructure]
status: resolved
duration_minutes: 116
author: Platform Engineering
---

# 2025-01-30 - Disk Space Exhaustion in payment-gateway

## Summary

On 2025-01-30, the payment-gateway service experienced an infrastructure failure affecting Azure Functions. The incident lasted approximately 116 minutes and affected 1620 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 12:00 | Monitoring alert triggered |
| 12:02 | On-call engineer paged |
| 12:05 | Initial investigation started |
| 12:10 | Root cause identified |
| 13:09 | Mitigation applied |
| 13:32 | Service recovery observed |
| 13:56 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in Azure Functions. During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-payment-gateway-prod
- Region: westeurope


## Impact


- Service degradation: 96% of requests affected
- Error rate spike: 29% (baseline: <1%)
- Latency increase: p99 went from 206ms to 5954ms


### Affected Services
- payment-gateway
- auth-service

### Customer Impact

- 2684 customer-facing errors
- 28 support tickets created
- Estimated revenue impact: $28223


## Resolution


1. Reverted the configuration change in Azure Functions
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
| P1 | Implement monitoring for disk space exhaustion | Platform Engineering | 2025-02-06 |
| P2 | Update runbook | SRE | 2025-02-13 |
| P2 | Add load test scenario | DevOps | 2025-02-20 |
| P3 | Review similar services | Database Team | 2025-03-01 |


## Related Incidents


- [[2025-01-30-previous-incident|Previous infrastructure incident]]
- [[runbook-payment-gateway|payment-gateway Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by Platform Engineering on 2025-02-02*
