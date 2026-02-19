---
title: "2025-12-07 - Disk Space Exhaustion in order-service"
date: 2025-12-07
severity: P1
services: [order-service, auth-service, analytics-pipeline]
tags: [rca, p1, infrastructure]
status: resolved
duration_minutes: 30
author: SRE
---

# 2025-12-07 - Disk Space Exhaustion in order-service

## Summary

On 2025-12-07, the order-service service experienced an infrastructure failure affecting Azure Storage. The incident lasted approximately 30 minutes and affected 8687 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 03:53 | Monitoring alert triggered |
| 03:55 | On-call engineer paged |
| 03:58 | Initial investigation started |
| 04:03 | Root cause identified |
| 04:11 | Mitigation applied |
| 04:17 | Service recovery observed |
| 04:23 | Incident resolved |

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


- Service degradation: 58% of requests affected
- Error rate spike: 30% (baseline: <1%)
- Latency increase: p99 went from 333ms to 4939ms


### Affected Services
- order-service
- auth-service
- analytics-pipeline

### Customer Impact

- 1673 customer-facing errors
- 64 support tickets created
- Estimated revenue impact: $14106


## Resolution


1. Reverted the configuration change in Azure Storage
2. Implemented infrastructure-as-code for all changes
3. Updated deployment checklist
4. Added configuration validation in CI/CD pipeline


## Lessons Learned

### What Went Well

- Alert fired within 2 minutes of incident start
- On-call response was quick (7 minutes)
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
| P1 | Implement monitoring for disk space exhaustion | Database Team | 2025-12-14 |
| P2 | Update runbook | Platform Engineering | 2025-12-21 |
| P2 | Add load test scenario | DevOps | 2025-12-28 |
| P3 | Review similar services | Database Team | 2026-01-06 |


## Related Incidents


- [[2025-12-07-previous-incident|Previous infrastructure incident]]
- [[runbook-order-service|order-service Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by SRE on 2025-12-12*
