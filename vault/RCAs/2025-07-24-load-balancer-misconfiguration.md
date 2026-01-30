---
title: "2025-07-24 - Load Balancer Misconfiguration in auth-service"
date: 2025-07-24
severity: P2
services: [auth-service]
tags: [rca, p2, infrastructure]
status: resolved
duration_minutes: 167
author: SRE
---

# 2025-07-24 - Load Balancer Misconfiguration in auth-service

## Summary

On 2025-07-24, the auth-service service experienced an infrastructure failure affecting Azure CDN. The incident lasted approximately 167 minutes and affected 7796 users and 1 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 12:14 | Monitoring alert triggered |
| 12:16 | On-call engineer paged |
| 12:19 | Initial investigation started |
| 12:24 | Root cause identified |
| 13:54 | Mitigation applied |
| 14:27 | Service recovery observed |
| 15:01 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in Azure CDN. During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-auth-service-prod
- Region: westeurope


## Impact


- Service degradation: 81% of requests affected
- Error rate spike: 25% (baseline: <1%)
- Latency increase: p99 went from 432ms to 5134ms


### Affected Services
- auth-service

### Customer Impact

- 4350 customer-facing errors
- 100 support tickets created
- Estimated revenue impact: $25152


## Resolution


1. Reverted the configuration change in Azure CDN
2. Implemented infrastructure-as-code for all changes
3. Updated deployment checklist
4. Added configuration validation in CI/CD pipeline


## Lessons Learned

### What Went Well

- Alert fired within 4 minutes of incident start
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
| P1 | Implement monitoring for load balancer misconfiguration | SRE | 2025-07-31 |
| P2 | Update runbook | Platform Engineering | 2025-08-07 |
| P2 | Add load test scenario | SRE | 2025-08-14 |
| P3 | Review similar services | Backend Team | 2025-08-23 |


## Related Incidents


- [[2025-07-24-previous-incident|Previous infrastructure incident]]
- [[runbook-auth-service|auth-service Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by SRE on 2025-07-26*
