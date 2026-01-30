---
title: "2025-03-01 - Kubernetes Pod Crash Loop in analytics-pipeline"
date: 2025-03-01
severity: P1
services: [analytics-pipeline, payment-gateway]
tags: [rca, p1, container]
status: resolved
duration_minutes: 160
author: Infrastructure
---

# 2025-03-01 - Kubernetes Pod Crash Loop in analytics-pipeline

## Summary

On 2025-03-01, the analytics-pipeline service experienced a Kubernetes pod crash loop. The incident lasted approximately 160 minutes and affected 2737 users and 2 dependent services.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 10:48 | Monitoring alert triggered |
| 10:50 | On-call engineer paged |
| 10:53 | Initial investigation started |
| 10:58 | Root cause identified |
| 12:24 | Mitigation applied |
| 12:56 | Service recovery observed |
| 13:28 | Incident resolved |

## Root Cause


Pods in the analytics-pipeline deployment entered a CrashLoopBackOff state due to a resource constraint issue.

```yaml
# Pod status
Name: analytics-pipeline-7b9d4f8c6-x2k9m
Status: CrashLoopBackOff
Restart Count: 37
Last State: OOMKilled
```

Key factors:
1. Memory limits were set too low for the new version
2. JVM heap size was not configured correctly
3. No resource quotas were enforced at namespace level


## Impact


- Service degradation: 88% of requests affected
- Error rate spike: 37% (baseline: <1%)
- Latency increase: p99 went from 461ms to 9424ms


### Affected Services
- analytics-pipeline
- payment-gateway

### Customer Impact

- 3006 customer-facing errors
- 43 support tickets created
- Estimated revenue impact: $17765


## Resolution


1. Increased memory limits from 428Mi to 1147Mi
2. Configured JVM heap size to 75% of container memory
3. Implemented resource monitoring with alerts
4. Added memory profiling to staging tests


## Lessons Learned

### What Went Well

- Alert fired within 5 minutes of incident start
- On-call response was quick (6 minutes)
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
| P1 | Implement monitoring for kubernetes pod crash loop | Platform Engineering | 2025-03-08 |
| P2 | Update runbook | Database Team | 2025-03-15 |
| P2 | Add load test scenario | SRE | 2025-03-22 |
| P3 | Review similar services | Platform Engineering | 2025-03-31 |


## Related Incidents


- [[2025-03-01-previous-incident|Previous container incident]]
- [[runbook-analytics-pipeline|analytics-pipeline Runbook]]
- [[architecture-container|Container Architecture]]


---
*RCA prepared by Infrastructure on 2025-03-02*
