---
title: "2025-04-01 - Disk Space Exhaustion in recommendation-engine"
date: 2025-04-01
severity: P1
services: [recommendation-engine, auth-service, payment-gateway, inventory-api]
tags: [rca, p1, infrastructure]
status: resolved
duration_minutes: 82
author: Backend Team
---

# 2025-04-01 - Disk Space Exhaustion in recommendation-engine

## Summary

On 2025-04-01, the recommendation-engine service experienced an infrastructure failure affecting Azure Storage. The incident lasted approximately 82 minutes and affected 9743 users and 4 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 20:40 | Monitoring alert triggered |
| 20:42 | On-call engineer paged |
| 20:45 | Initial investigation started |
| 20:50 | Root cause identified |
| 21:29 | Mitigation applied |
| 21:45 | Service recovery observed |
| 22:02 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in Azure Storage. During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-recommendation-engine-prod
- Region: westus2


## Impact


- Service degradation: 72% of requests affected
- Error rate spike: 30% (baseline: <1%)
- Latency increase: p99 went from 227ms to 7108ms


### Affected Services
- recommendation-engine
- auth-service
- payment-gateway
- inventory-api

### Customer Impact

- 1405 customer-facing errors
- 16 support tickets created
- Estimated revenue impact: $46168


## Resolution


1. Reverted the configuration change in Azure Storage
2. Implemented infrastructure-as-code for all changes
3. Updated deployment checklist
4. Added configuration validation in CI/CD pipeline


## Lessons Learned

### What Went Well

- Alert fired within 4 minutes of incident start
- On-call response was quick (3 minutes)
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
| P1 | Implement monitoring for disk space exhaustion | SRE | 2025-04-08 |
| P2 | Update runbook | SRE | 2025-04-15 |
| P2 | Add load test scenario | SRE | 2025-04-22 |
| P3 | Review similar services | Backend Team | 2025-05-01 |


## Related Incidents


- [[2025-04-01-previous-incident|Previous infrastructure incident]]
- [[runbook-recommendation-engine|recommendation-engine Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by Backend Team on 2025-04-06*
