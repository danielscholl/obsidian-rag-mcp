---
title: "2025-03-18 - Certificate Expiration in analytics-pipeline"
date: 2025-03-18
severity: P1
services: [analytics-pipeline, inventory-api, notification-service]
tags: [rca, p1, infrastructure]
status: resolved
duration_minutes: 147
author: SRE
---

# 2025-03-18 - Certificate Expiration in analytics-pipeline

## Summary

On 2025-03-18, the analytics-pipeline service experienced an infrastructure failure affecting Azure Storage. The incident lasted approximately 147 minutes and affected 8489 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 03:54 | Monitoring alert triggered |
| 03:56 | On-call engineer paged |
| 03:59 | Initial investigation started |
| 04:04 | Root cause identified |
| 05:22 | Mitigation applied |
| 05:51 | Service recovery observed |
| 06:21 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in Azure Storage. During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-analytics-pipeline-prod
- Region: westus2


## Impact


- Service degradation: 73% of requests affected
- Error rate spike: 41% (baseline: <1%)
- Latency increase: p99 went from 471ms to 9094ms


### Affected Services
- analytics-pipeline
- inventory-api
- notification-service

### Customer Impact

- 868 customer-facing errors
- 82 support tickets created
- Estimated revenue impact: $46841


## Resolution


1. Reverted the configuration change in Azure Storage
2. Implemented infrastructure-as-code for all changes
3. Updated deployment checklist
4. Added configuration validation in CI/CD pipeline


## Lessons Learned

### What Went Well

- Alert fired within 1 minutes of incident start
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
| P1 | Implement monitoring for certificate expiration | Database Team | 2025-03-25 |
| P2 | Update runbook | Platform Engineering | 2025-04-01 |
| P2 | Add load test scenario | DevOps | 2025-04-08 |
| P3 | Review similar services | Database Team | 2025-04-17 |


## Related Incidents


- [[2025-03-18-previous-incident|Previous infrastructure incident]]
- [[runbook-analytics-pipeline|analytics-pipeline Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by SRE on 2025-03-20*
