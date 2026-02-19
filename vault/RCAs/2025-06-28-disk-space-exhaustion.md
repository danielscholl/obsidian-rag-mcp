---
title: "2025-06-28 - Disk Space Exhaustion in user-service"
date: 2025-06-28
severity: P1
services: [user-service, search-api, recommendation-engine, analytics-pipeline]
tags: [rca, p1, infrastructure]
status: resolved
duration_minutes: 152
author: Database Team
---

# 2025-06-28 - Disk Space Exhaustion in user-service

## Summary

On 2025-06-28, the user-service service experienced an infrastructure failure affecting AKS (Kubernetes). The incident lasted approximately 152 minutes and affected 7453 users and 4 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 00:36 | Monitoring alert triggered |
| 00:38 | On-call engineer paged |
| 00:41 | Initial investigation started |
| 00:46 | Root cause identified |
| 02:07 | Mitigation applied |
| 02:37 | Service recovery observed |
| 03:08 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in AKS (Kubernetes). During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-user-service-prod
- Region: eastus


## Impact


- Service degradation: 70% of requests affected
- Error rate spike: 36% (baseline: <1%)
- Latency increase: p99 went from 261ms to 8879ms


### Affected Services
- user-service
- search-api
- recommendation-engine
- analytics-pipeline

### Customer Impact

- 3430 customer-facing errors
- 75 support tickets created
- Estimated revenue impact: $21477


## Resolution


1. Reverted the configuration change in AKS (Kubernetes)
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
| P1 | Implement monitoring for disk space exhaustion | Database Team | 2025-07-05 |
| P2 | Update runbook | DevOps | 2025-07-12 |
| P2 | Add load test scenario | SRE | 2025-07-19 |
| P3 | Review similar services | Infrastructure | 2025-07-28 |


## Related Incidents


- [[2025-06-28-previous-incident|Previous infrastructure incident]]
- [[runbook-user-service|user-service Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by Database Team on 2025-07-02*
