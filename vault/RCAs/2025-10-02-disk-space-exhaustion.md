---
title: "2025-10-02 - Disk Space Exhaustion in analytics-pipeline"
date: 2025-10-02
severity: P1
services: [analytics-pipeline, auth-service]
tags: [rca, p1, infrastructure]
status: resolved
duration_minutes: 36
author: Database Team
---

# 2025-10-02 - Disk Space Exhaustion in analytics-pipeline

## Summary

On 2025-10-02, the analytics-pipeline service experienced an infrastructure failure affecting Azure Service Bus. The incident lasted approximately 36 minutes and affected 6066 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 00:50 | Monitoring alert triggered |
| 00:52 | On-call engineer paged |
| 00:55 | Initial investigation started |
| 01:00 | Root cause identified |
| 01:11 | Mitigation applied |
| 01:18 | Service recovery observed |
| 01:26 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in Azure Service Bus. During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-analytics-pipeline-prod
- Region: westus2


## Impact


- Service degradation: 63% of requests affected
- Error rate spike: 50% (baseline: <1%)
- Latency increase: p99 went from 171ms to 7537ms


### Affected Services
- analytics-pipeline
- auth-service

### Customer Impact

- 891 customer-facing errors
- 85 support tickets created
- Estimated revenue impact: $44599


## Resolution


1. Reverted the configuration change in Azure Service Bus
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
| P1 | Implement monitoring for disk space exhaustion | Database Team | 2025-10-09 |
| P2 | Update runbook | Backend Team | 2025-10-16 |
| P2 | Add load test scenario | Database Team | 2025-10-23 |
| P3 | Review similar services | Infrastructure | 2025-11-01 |


## Related Incidents


- [[2025-10-02-previous-incident|Previous infrastructure incident]]
- [[runbook-analytics-pipeline|analytics-pipeline Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by Database Team on 2025-10-07*
