---
title: "billing-api Service"
tags: [service, billing-api, documentation]
status: active
---

# billing-api

## Purpose

The billing-api handles core functionality for our platform.

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
kubectl apply -f k8s/billing-api/
```

## Monitoring

- Metrics: Prometheus
- Logs: Azure Log Analytics
- Traces: Application Insights

## See Also

- [[runbook-billing-api|Operational Runbook]]
- [[rca-billing-api|Past Incidents]]
