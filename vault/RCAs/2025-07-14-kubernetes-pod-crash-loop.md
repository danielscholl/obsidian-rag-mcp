---
title: "2025-07-14 - Kubernetes Pod Crash Loop in auth-service"
date: 2025-07-14
severity: P1
services: [auth-service, order-service]
tags: [rca, p1, container]
status: resolved
duration_minutes: 166
author: Platform Engineering
---

# 2025-07-14 - Kubernetes Pod Crash Loop in auth-service

## Summary

On 2025-07-14, the auth-service service experienced a Kubernetes pod crash loop. The incident lasted approximately 166 minutes and affected 4133 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 16:25 | Monitoring alert triggered |
| 16:27 | On-call engineer paged |
| 16:30 | Initial investigation started |
| 16:35 | Root cause identified |
| 18:04 | Mitigation applied |
| 18:37 | Service recovery observed |
| 19:11 | Incident resolved |

## Root Cause


Pods in the auth-service deployment entered a CrashLoopBackOff state due to a resource constraint issue.

```yaml
# Pod status
Name: auth-service-7b9d4f8c6-x2k9m
Status: CrashLoopBackOff
Restart Count: 43
Last State: OOMKilled
```

Key factors:
1. Memory limits were set too low for the new version
2. JVM heap size was not configured correctly
3. No resource quotas were enforced at namespace level


## Impact


- Service degradation: 78% of requests affected
- Error rate spike: 36% (baseline: <1%)
- Latency increase: p99 went from 431ms to 6939ms


### Affected Services
- auth-service
- order-service

### Customer Impact

- 1498 customer-facing errors
- 90 support tickets created
- Estimated revenue impact: $44202


## Resolution


1. Increased memory limits from 397Mi to 1215Mi
2. Configured JVM heap size to 75% of container memory
3. Implemented resource monitoring with alerts
4. Added memory profiling to staging tests


## Lessons Learned

### What Went Well

- Alert fired within 2 minutes of incident start
- On-call response was quick (8 minutes)
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
| P1 | Implement monitoring for kubernetes pod crash loop | Infrastructure | 2025-07-21 |
| P2 | Update runbook | Platform Engineering | 2025-07-28 |
| P2 | Add load test scenario | Database Team | 2025-08-04 |
| P3 | Review similar services | Database Team | 2025-08-13 |


## Related Incidents


- [[2025-07-14-previous-incident|Previous container incident]]
- [[runbook-auth-service|auth-service Runbook]]
- [[architecture-container|Container Architecture]]


---
*RCA prepared by Platform Engineering on 2025-07-18*
