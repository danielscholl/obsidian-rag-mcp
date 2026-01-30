---
title: "2025-10-05 - Kubernetes Pod Crash Loop in user-service"
date: 2025-10-05
severity: P1
services: [user-service, auth-service, payment-gateway, analytics-pipeline]
tags: [rca, p1, container]
status: resolved
duration_minutes: 50
author: SRE
---

# 2025-10-05 - Kubernetes Pod Crash Loop in user-service

## Summary

On 2025-10-05, the user-service service experienced a Kubernetes pod crash loop. The incident lasted approximately 50 minutes and affected 100 users and 4 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 17:17 | Monitoring alert triggered |
| 17:19 | On-call engineer paged |
| 17:22 | Initial investigation started |
| 17:27 | Root cause identified |
| 17:47 | Mitigation applied |
| 17:57 | Service recovery observed |
| 18:07 | Incident resolved |

## Root Cause


Pods in the user-service deployment entered a CrashLoopBackOff state due to a resource constraint issue.

```yaml
# Pod status
Name: user-service-7b9d4f8c6-x2k9m
Status: CrashLoopBackOff
Restart Count: 34
Last State: OOMKilled
```

Key factors:
1. Memory limits were set too low for the new version
2. JVM heap size was not configured correctly
3. No resource quotas were enforced at namespace level


## Impact


- Service degradation: 70% of requests affected
- Error rate spike: 43% (baseline: <1%)
- Latency increase: p99 went from 128ms to 3993ms


### Affected Services
- user-service
- auth-service
- payment-gateway
- analytics-pipeline

### Customer Impact

- 1804 customer-facing errors
- 59 support tickets created
- Estimated revenue impact: $33203


## Resolution


1. Increased memory limits from 438Mi to 1024Mi
2. Configured JVM heap size to 75% of container memory
3. Implemented resource monitoring with alerts
4. Added memory profiling to staging tests


## Lessons Learned

### What Went Well

- Alert fired within 1 minutes of incident start
- On-call response was quick (4 minutes)
- Cross-team collaboration was effective
- Communication to stakeholders was timely


### What Could Be Improved  

- Need better runbooks for container issues
- Monitoring coverage gaps identified
- Load testing should cover this scenario
- Need automated rollback for faster recovery


## Action Items


| Priority | Action | Owner | Due Date |
|----------|--------|-------|----------|
| P1 | Implement monitoring for kubernetes pod crash loop | Database Team | 2025-10-12 |
| P2 | Update runbook | Platform Engineering | 2025-10-19 |
| P2 | Add load test scenario | Infrastructure | 2025-10-26 |
| P3 | Review similar services | SRE | 2025-11-04 |


## Related Incidents


- [[2025-10-05-previous-incident|Previous container incident]]
- [[runbook-user-service|user-service Runbook]]
- [[architecture-container|Container Architecture]]


---
*RCA prepared by SRE on 2025-10-10*
