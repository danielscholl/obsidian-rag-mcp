---
title: "2025-10-21 - Load Balancer Misconfiguration in order-service"
date: 2025-10-21
severity: P2
services: [order-service, search-api, recommendation-engine, auth-service]
tags: [rca, p2, infrastructure]
status: resolved
duration_minutes: 133
author: Backend Team
---

# 2025-10-21 - Load Balancer Misconfiguration in order-service

## Summary

On 2025-10-21, the order-service service experienced an infrastructure failure affecting Azure Storage. The incident lasted approximately 133 minutes and affected 694 users and 4 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 22:58 | Monitoring alert triggered |
| 23:00 | On-call engineer paged |
| 23:03 | Initial investigation started |
| 23:08 | Root cause identified |
| 00:17 | Mitigation applied |
| 00:44 | Service recovery observed |
| 01:11 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in Azure Storage. During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-order-service-prod
- Region: eastus


## Impact


- Service degradation: 93% of requests affected
- Error rate spike: 48% (baseline: <1%)
- Latency increase: p99 went from 367ms to 4367ms


### Affected Services
- order-service
- search-api
- recommendation-engine
- auth-service

### Customer Impact

- 1777 customer-facing errors
- 46 support tickets created
- Estimated revenue impact: $26905


## Resolution


1. Reverted the configuration change in Azure Storage
2. Implemented infrastructure-as-code for all changes
3. Updated deployment checklist
4. Added configuration validation in CI/CD pipeline


## Lessons Learned

### What Went Well

- Alert fired within 3 minutes of incident start
- On-call response was quick (8 minutes)
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
| P1 | Implement monitoring for load balancer misconfiguration | Platform Engineering | 2025-10-28 |
| P2 | Update runbook | DevOps | 2025-11-04 |
| P2 | Add load test scenario | Database Team | 2025-11-11 |
| P3 | Review similar services | Infrastructure | 2025-11-20 |


## Related Incidents


- [[2025-10-21-previous-incident|Previous infrastructure incident]]
- [[runbook-order-service|order-service Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by Backend Team on 2025-10-26*
