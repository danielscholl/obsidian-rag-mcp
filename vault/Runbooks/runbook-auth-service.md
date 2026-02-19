---
title: "auth-service Runbook"
tags: [runbook, auth-service, operations]
last_updated: 2026-01-29
---

# auth-service Runbook

## Overview

The auth-service is a critical component of our platform. This runbook provides operational guidance for common issues.

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   auth-ser  │────▶│  Database   │
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
1. Check database connection pool: `kubectl exec -it auth-service-xxx -- curl localhost:8080/actuator/health`
2. Review recent deployments
3. Check downstream service health

**Resolution:**
1. Scale horizontally if needed: `kubectl scale deployment auth-service --replicas=5`
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
1. Restart pods: `kubectl rollout restart deployment auth-service`
2. Increase memory limits if justified
3. Profile application for leaks

## Monitoring

- Grafana Dashboard: https://grafana.internal/d/auth-service
- Alerts: #auth-service-alerts Slack channel
- Logs: `kubectl logs -l app=auth-service --tail=100`

## Contacts

- On-call: #auth-service-oncall
- Team: #auth-service-team
- Escalation: Platform Engineering

## Related Documents

- [[architecture-auth-service|Architecture Overview]]
- [[deployment-auth-service|Deployment Guide]]
