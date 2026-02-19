---
title: "2025-04-27 - Load Balancer Misconfiguration in analytics-pipeline"
date: 2025-04-27
severity: P2
services: [analytics-pipeline, order-service, notification-service]
tags: [rca, p2, infrastructure]
status: resolved
duration_minutes: 141
author: SRE
---

# 2025-04-27 - Load Balancer Misconfiguration in analytics-pipeline

## Summary

On 2025-04-27, the analytics-pipeline service experienced an infrastructure failure affecting Azure Storage. The incident lasted approximately 141 minutes and affected 9850 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 12:52 | Monitoring alert triggered |
| 12:54 | On-call engineer paged |
| 12:57 | Initial investigation started |
| 13:02 | Root cause identified |
| 14:16 | Mitigation applied |
| 14:44 | Service recovery observed |
| 15:13 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in Azure Storage. During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-analytics-pipeline-prod
- Region: eastus


## Impact


- Service degradation: 61% of requests affected
- Error rate spike: 16% (baseline: <1%)
- Latency increase: p99 went from 494ms to 2596ms


### Affected Services
- analytics-pipeline
- order-service
- notification-service

### Customer Impact

- 1003 customer-facing errors
- 87 support tickets created
- Estimated revenue impact: $49538


## Resolution


1. Reverted the configuration change in Azure Storage
2. Implemented infrastructure-as-code for all changes
3. Updated deployment checklist
4. Added configuration validation in CI/CD pipeline


## Lessons Learned

### What Went Well

- Alert fired within 1 minutes of incident start
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
| P1 | Implement monitoring for load balancer misconfiguration | Platform Engineering | 2025-05-04 |
| P2 | Update runbook | SRE | 2025-05-11 |
| P2 | Add load test scenario | SRE | 2025-05-18 |
| P3 | Review similar services | DevOps | 2025-05-27 |


## Related Incidents


- [[2025-04-27-previous-incident|Previous infrastructure incident]]
- [[runbook-analytics-pipeline|analytics-pipeline Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by SRE on 2025-04-28*
