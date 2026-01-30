---
title: "notification-service Service"
tags: [service, notification-service, documentation]
status: active
---

# notification-service

## Purpose

The notification-service handles core functionality for our platform.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/v1/resource | GET | List resources |
| /api/v1/resource/:id | GET | Get resource by ID |
| /api/v1/resource | POST | Create resource |
| /api/v1/health | GET | Health check |

## Dependencies

- Database: PostgreSQL
- Cache: Redis
- Message Queue: Azure Service Bus

## Configuration

Key environment variables:
- `DATABASE_URL`: Connection string
- `REDIS_URL`: Cache connection
- `LOG_LEVEL`: Logging verbosity

## Deployment

Deployed to AKS via GitHub Actions.

```bash
# Manual deployment
kubectl apply -f k8s/notification-service/
```

## Monitoring

- Metrics: Prometheus
- Logs: Azure Log Analytics
- Traces: Application Insights

## See Also

- [[runbook-notification-service|Operational Runbook]]
- [[rca-notification-service|Past Incidents]]
