---
title: "billing-api Runbook"
tags: [runbook, billing-api, operations]
last_updated: 2026-01-29
---

# billing-api Runbook

## Overview

The billing-api is a critical component of our platform. This runbook provides operational guidance for common issues.

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   billing-  │────▶│  Database   │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Cache     │
                    └─────────────┘
```

## Common Issues

### High Latency

**Symptoms:**
- p99 latency > 500ms
- Increased error rate

**Diagnosis:**
1. Check database connection pool: `kubectl exec -it billing-api-xxx -- curl localhost:8080/actuator/health`
2. Review recent deployments
3. Check downstream service health

**Resolution:**
1. Scale horizontally if needed: `kubectl scale deployment billing-api --replicas=5`
2. Check for slow queries in database
3. Verify cache hit rate

### Memory Issues

**Symptoms:**
- OOMKilled pods
- Increasing memory usage over time

**Diagnosis:**
1. Check memory metrics in Grafana
2. Review heap dumps if available
3. Check for memory leaks in recent changes

**Resolution:**
1. Restart pods: `kubectl rollout restart deployment billing-api`
2. Increase memory limits if justified
3. Profile application for leaks

## Monitoring

- Grafana Dashboard: https://grafana.internal/d/billing-api
- Alerts: #billing-api-alerts Slack channel
- Logs: `kubectl logs -l app=billing-api --tail=100`

## Contacts

- On-call: #billing-api-oncall
- Team: #billing-api-team
- Escalation: Platform Engineering

## Related Documents

- [[architecture-billing-api|Architecture Overview]]
- [[deployment-billing-api|Deployment Guide]]
