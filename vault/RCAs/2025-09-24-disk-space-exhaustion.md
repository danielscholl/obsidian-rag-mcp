---
title: "2025-09-24 - Disk Space Exhaustion in recommendation-engine"
date: 2025-09-24
severity: P1
services: [user-service, recommendation-engine]
tags: [rca, p1, infrastructure]
status: resolved
duration_minutes: 137
author: Infrastructure
---

# 2025-09-24 - Disk Space Exhaustion in recommendation-engine

## Summary

On 2025-09-24, the recommendation-engine service experienced an infrastructure failure affecting Azure Service Bus. The incident lasted approximately 137 minutes and affected 5553 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 04:13 | Monitoring alert triggered |
| 04:15 | On-call engineer paged |
| 04:18 | Initial investigation started |
| 04:23 | Root cause identified |
| 05:35 | Mitigation applied |
| 06:02 | Service recovery observed |
| 06:30 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in Azure Service Bus. During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-recommendation-engine-prod
- Region: eastus


## Impact


- Service degradation: 69% of requests affected
- Error rate spike: 33% (baseline: <1%)
- Latency increase: p99 went from 197ms to 9191ms


### Affected Services
- user-service
- recommendation-engine

### Customer Impact

- 3987 customer-facing errors
- 98 support tickets created
- Estimated revenue impact: $16521


## Resolution


1. Reverted the configuration change in Azure Service Bus
2. Implemented infrastructure-as-code for all changes
3. Updated deployment checklist
4. Added configuration validation in CI/CD pipeline


## Lessons Learned

### What Went Well

- Alert fired within 1 minutes of incident start
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
| P1 | Implement monitoring for disk space exhaustion | DevOps | 2025-10-01 |
| P2 | Update runbook | Platform Engineering | 2025-10-08 |
| P2 | Add load test scenario | DevOps | 2025-10-15 |
| P3 | Review similar services | Database Team | 2025-10-24 |


## Related Incidents


- [[2025-09-24-previous-incident|Previous infrastructure incident]]
- [[runbook-recommendation-engine|recommendation-engine Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by Infrastructure on 2025-09-26*
