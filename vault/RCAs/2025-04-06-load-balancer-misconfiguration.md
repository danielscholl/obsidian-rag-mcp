---
title: "2025-04-06 - Load Balancer Misconfiguration in notification-service"
date: 2025-04-06
severity: P2
services: [notification-service, payment-gateway]
tags: [rca, p2, infrastructure]
status: resolved
duration_minutes: 33
author: Platform Engineering
---

# 2025-04-06 - Load Balancer Misconfiguration in notification-service

## Summary

On 2025-04-06, the notification-service service experienced an infrastructure failure affecting Azure CDN. The incident lasted approximately 33 minutes and affected 9547 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 14:23 | Monitoring alert triggered |
| 14:25 | On-call engineer paged |
| 14:28 | Initial investigation started |
| 14:33 | Root cause identified |
| 14:42 | Mitigation applied |
| 14:49 | Service recovery observed |
| 14:56 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in Azure CDN. During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-notification-service-prod
- Region: westus2


## Impact


- Service degradation: 52% of requests affected
- Error rate spike: 10% (baseline: <1%)
- Latency increase: p99 went from 112ms to 4570ms


### Affected Services
- notification-service
- payment-gateway

### Customer Impact

- 408 customer-facing errors
- 75 support tickets created
- Estimated revenue impact: $26696


## Resolution


1. Reverted the configuration change in Azure CDN
2. Implemented infrastructure-as-code for all changes
3. Updated deployment checklist
4. Added configuration validation in CI/CD pipeline


## Lessons Learned

### What Went Well

- Alert fired within 2 minutes of incident start
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
| P1 | Implement monitoring for load balancer misconfiguration | Infrastructure | 2025-04-13 |
| P2 | Update runbook | DevOps | 2025-04-20 |
| P2 | Add load test scenario | SRE | 2025-04-27 |
| P3 | Review similar services | Infrastructure | 2025-05-06 |


## Related Incidents


- [[2025-04-06-previous-incident|Previous infrastructure incident]]
- [[runbook-notification-service|notification-service Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by Platform Engineering on 2025-04-09*
