---
title: "2025-12-13 - Disk Space Exhaustion in recommendation-engine"
date: 2025-12-13
severity: P1
services: [recommendation-engine, payment-gateway, order-service]
tags: [rca, p1, infrastructure]
status: resolved
duration_minutes: 162
author: Infrastructure
---

# 2025-12-13 - Disk Space Exhaustion in recommendation-engine

## Summary

On 2025-12-13, the recommendation-engine service experienced an infrastructure failure affecting Azure Functions. The incident lasted approximately 162 minutes and affected 2862 users and 3 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 16:28 | Monitoring alert triggered |
| 16:30 | On-call engineer paged |
| 16:33 | Initial investigation started |
| 16:38 | Root cause identified |
| 18:05 | Mitigation applied |
| 18:37 | Service recovery observed |
| 19:10 | Incident resolved |

## Root Cause


The incident was caused by a misconfiguration in Azure Functions. During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-recommendation-engine-prod
- Region: westus2


## Impact


- Service degradation: 100% of requests affected
- Error rate spike: 25% (baseline: <1%)
- Latency increase: p99 went from 267ms to 4185ms


### Affected Services
- recommendation-engine
- payment-gateway
- order-service

### Customer Impact

- 535 customer-facing errors
- 23 support tickets created
- Estimated revenue impact: $12315


## Resolution


1. Reverted the configuration change in Azure Functions
2. Implemented infrastructure-as-code for all changes
3. Updated deployment checklist
4. Added configuration validation in CI/CD pipeline


## Lessons Learned

### What Went Well

- Alert fired within 2 minutes of incident start
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
| P1 | Implement monitoring for disk space exhaustion | Infrastructure | 2025-12-20 |
| P2 | Update runbook | Database Team | 2025-12-27 |
| P2 | Add load test scenario | Backend Team | 2026-01-03 |
| P3 | Review similar services | Platform Engineering | 2026-01-12 |


## Related Incidents


- [[2025-12-13-previous-incident|Previous infrastructure incident]]
- [[runbook-recommendation-engine|recommendation-engine Runbook]]
- [[architecture-infrastructure|Infrastructure Architecture]]


---
*RCA prepared by Infrastructure on 2025-12-17*
