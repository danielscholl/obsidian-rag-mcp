#!/usr/bin/env python3
"""
Generate sample RCA documents for testing the RAG system.

Creates realistic DevOps RCA reports covering common scenarios:
- Database issues (timeouts, connection pools, deadlocks)
- Cloud infrastructure (Azure, AWS, GCP)
- Microservice failures
- Network issues
- Deployment problems
- Kubernetes/container issues
"""

import random
from datetime import datetime, timedelta
from pathlib import Path

# Sample data for generating RCAs
SERVICES = [
    "billing-api",
    "user-service",
    "payment-gateway",
    "notification-service",
    "inventory-api",
    "order-service",
    "auth-service",
    "search-api",
    "analytics-pipeline",
    "recommendation-engine",
]

DATABASES = [
    "CosmosDB",
    "PostgreSQL",
    "Redis",
    "MongoDB",
    "Elasticsearch",
    "SQL Server",
]

CLOUD_SERVICES = [
    "Azure App Service",
    "Azure Functions",
    "AKS (Kubernetes)",
    "Azure Service Bus",
    "Azure Event Hub",
    "Azure Storage",
    "Azure CDN",
    "Application Gateway",
]

ISSUE_TYPES = [
    ("Database Connection Pool Exhaustion", "database", "P1"),
    ("Query Timeout Under Load", "database", "P2"),
    ("Deadlock in Transaction", "database", "P2"),
    ("Memory Leak in Service", "application", "P2"),
    ("Certificate Expiration", "infrastructure", "P1"),
    ("DNS Resolution Failure", "network", "P1"),
    ("Load Balancer Misconfiguration", "infrastructure", "P2"),
    ("Deployment Rollback Required", "deployment", "P2"),
    ("Kubernetes Pod Crash Loop", "container", "P1"),
    ("Rate Limiting Triggered", "application", "P3"),
    ("Third-Party API Degradation", "external", "P2"),
    ("Disk Space Exhaustion", "infrastructure", "P1"),
    ("SSL/TLS Handshake Failure", "network", "P2"),
    ("Message Queue Backlog", "messaging", "P2"),
    ("Cache Invalidation Bug", "application", "P3"),
]

TEAMS = [
    "Platform Engineering",
    "Backend Team",
    "DevOps",
    "SRE",
    "Infrastructure",
    "Database Team",
]

RCA_TEMPLATE = '''---
title: "{title}"
date: {date}
severity: {severity}
services: [{services}]
tags: [rca, {severity_tag}, {category}]
status: resolved
duration_minutes: {duration}
author: {author}
---

# {title}

## Summary

On {date}, the {primary_service} service experienced {issue_description}. The incident lasted approximately {duration} minutes and affected {impact}.

## Timeline

| Time (UTC) | Event |
|------------|-------|
{timeline}

## Root Cause

{root_cause}

## Impact

{impact_detail}

### Affected Services
{affected_services_list}

### Customer Impact
{customer_impact}

## Resolution

{resolution}

## Lessons Learned

### What Went Well
{went_well}

### What Could Be Improved  
{improvements}

## Action Items

{action_items}

## Related Incidents

{related}

---
*RCA prepared by {author} on {report_date}*
'''

def generate_timeline(start_time: datetime, duration: int) -> str:
    """Generate a realistic incident timeline."""
    events = [
        (0, "Monitoring alert triggered"),
        (2, "On-call engineer paged"),
        (5, "Initial investigation started"),
        (10, "Root cause identified"),
        (int(duration * 0.6), "Mitigation applied"),
        (int(duration * 0.8), "Service recovery observed"),
        (duration, "Incident resolved"),
    ]

    lines = []
    for offset, event in events:
        time = start_time + timedelta(minutes=offset)
        lines.append(f"| {time.strftime('%H:%M')} | {event} |")

    return "\n".join(lines)


def generate_rca(index: int, base_date: datetime) -> tuple[str, str]:
    """Generate a single RCA document."""

    issue_type, category, severity = random.choice(ISSUE_TYPES)
    primary_service = random.choice(SERVICES)
    affected_services = random.sample(SERVICES, random.randint(1, 3))
    if primary_service not in affected_services:
        affected_services.insert(0, primary_service)

    database = random.choice(DATABASES) if category == "database" else None
    cloud_service = random.choice(CLOUD_SERVICES) if category == "infrastructure" else None

    duration = random.randint(15, 180)
    incident_date = base_date - timedelta(days=random.randint(1, 365))

    # Generate content based on issue type
    if category == "database":
        issue_description = f"a {issue_type.lower()} in {database}"
        root_cause = f"""
The root cause was traced to {database} connection handling. Under increased load from a marketing campaign, the connection pool ({random.randint(50, 200)} connections) became exhausted.

Key factors:
1. Connection timeout was set to {random.randint(30, 120)} seconds, too long for our use case
2. No connection pool monitoring was in place
3. The service was holding connections during long-running operations

Technical details:
```
Error: {database}Exception: Connection pool exhausted
Max pool size: {random.randint(50, 200)}
Active connections: {random.randint(200, 500)}
Waiting requests: {random.randint(100, 1000)}
```
"""
        resolution = f"""
1. Increased connection pool size from {random.randint(50, 100)} to {random.randint(200, 500)}
2. Reduced connection timeout from {random.randint(60, 120)}s to {random.randint(10, 30)}s  
3. Implemented connection pooling best practices
4. Added circuit breaker pattern for {database} calls
"""
    elif category == "infrastructure":
        issue_description = f"an infrastructure failure affecting {cloud_service}"
        root_cause = f"""
The incident was caused by a misconfiguration in {cloud_service}. During a routine deployment, a configuration change was applied that impacted service availability.

Key factors:
1. Configuration change was not properly reviewed
2. Staging environment did not match production
3. Rollback procedure was not documented

Azure Resource affected:
- Resource Group: rg-{primary_service}-prod
- Region: {random.choice(['eastus', 'westus2', 'westeurope'])}
"""
        resolution = f"""
1. Reverted the configuration change in {cloud_service}
2. Implemented infrastructure-as-code for all changes
3. Updated deployment checklist
4. Added configuration validation in CI/CD pipeline
"""
    elif category == "container":
        issue_description = "a Kubernetes pod crash loop"
        root_cause = f"""
Pods in the {primary_service} deployment entered a CrashLoopBackOff state due to a resource constraint issue.

```yaml
# Pod status
Name: {primary_service}-7b9d4f8c6-x2k9m
Status: CrashLoopBackOff
Restart Count: {random.randint(5, 50)}
Last State: OOMKilled
```

Key factors:
1. Memory limits were set too low for the new version
2. JVM heap size was not configured correctly
3. No resource quotas were enforced at namespace level
"""
        resolution = f"""
1. Increased memory limits from {random.randint(256, 512)}Mi to {random.randint(1024, 2048)}Mi
2. Configured JVM heap size to 75% of container memory
3. Implemented resource monitoring with alerts
4. Added memory profiling to staging tests
"""
    else:
        issue_description = f"a {issue_type.lower()}"
        root_cause = f"""
The incident was caused by {issue_type.lower()} in the {primary_service} service.

Investigation revealed multiple contributing factors:
1. Recent code changes introduced a regression
2. Test coverage did not include edge cases
3. Monitoring gaps delayed detection
"""
        resolution = """
1. Deployed hotfix to address the immediate issue
2. Added regression tests for the affected code path
3. Implemented additional monitoring and alerting
4. Updated runbook with troubleshooting steps
"""

    # Build the document
    title = f"{incident_date.strftime('%Y-%m-%d')} - {issue_type} in {primary_service}"

    content = RCA_TEMPLATE.format(
        title=title,
        date=incident_date.strftime("%Y-%m-%d"),
        severity=severity,
        services=", ".join(affected_services),
        severity_tag=severity.lower(),
        category=category,
        duration=duration,
        author=random.choice(TEAMS),
        primary_service=primary_service,
        issue_description=issue_description,
        impact=f"{random.randint(100, 10000)} users and {len(affected_services)} dependent services",
        timeline=generate_timeline(
            incident_date.replace(hour=random.randint(0, 23), minute=random.randint(0, 59)),
            duration
        ),
        root_cause=root_cause,
        impact_detail=f"""
- Service degradation: {random.randint(50, 100)}% of requests affected
- Error rate spike: {random.randint(10, 50)}% (baseline: <1%)
- Latency increase: p99 went from {random.randint(100, 500)}ms to {random.randint(2000, 10000)}ms
""",
        affected_services_list="\n".join(f"- {s}" for s in affected_services),
        customer_impact=f"""
- {random.randint(100, 5000)} customer-facing errors
- {random.randint(10, 100)} support tickets created
- Estimated revenue impact: ${random.randint(1000, 50000)}
""",
        resolution=resolution,
        went_well=f"""
- Alert fired within {random.randint(1, 5)} minutes of incident start
- On-call response was quick ({random.randint(2, 10)} minutes)
- Cross-team collaboration was effective
- Communication to stakeholders was timely
""",
        improvements=f"""
- Need better runbooks for {category} issues
- Monitoring coverage gaps identified
- Load testing should cover this scenario
- Need automated rollback for faster recovery
""",
        action_items=f"""
| Priority | Action | Owner | Due Date |
|----------|--------|-------|----------|
| P1 | Implement monitoring for {issue_type.lower()} | {random.choice(TEAMS)} | {(incident_date + timedelta(days=7)).strftime('%Y-%m-%d')} |
| P2 | Update runbook | {random.choice(TEAMS)} | {(incident_date + timedelta(days=14)).strftime('%Y-%m-%d')} |
| P2 | Add load test scenario | {random.choice(TEAMS)} | {(incident_date + timedelta(days=21)).strftime('%Y-%m-%d')} |
| P3 | Review similar services | {random.choice(TEAMS)} | {(incident_date + timedelta(days=30)).strftime('%Y-%m-%d')} |
""",
        related=f"""
- [[{incident_date.strftime('%Y-%m-%d')}-previous-incident|Previous {category} incident]]
- [[runbook-{primary_service}|{primary_service} Runbook]]
- [[architecture-{category}|{category.title()} Architecture]]
""",
        report_date=(incident_date + timedelta(days=random.randint(1, 5))).strftime("%Y-%m-%d"),
    )

    filename = f"{incident_date.strftime('%Y-%m-%d')}-{issue_type.lower().replace(' ', '-').replace('/', '-')}.md"

    return filename, content


def generate_runbook(service: str) -> tuple[str, str]:
    """Generate a service runbook."""
    content = f'''---
title: "{service} Runbook"
tags: [runbook, {service}, operations]
last_updated: {datetime.now().strftime('%Y-%m-%d')}
---

# {service} Runbook

## Overview

The {service} is a critical component of our platform. This runbook provides operational guidance for common issues.

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   {service[:8]:8s}  │────▶│  Database   │
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
1. Check database connection pool: `kubectl exec -it {service}-xxx -- curl localhost:8080/actuator/health`
2. Review recent deployments
3. Check downstream service health

**Resolution:**
1. Scale horizontally if needed: `kubectl scale deployment {service} --replicas=5`
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
1. Restart pods: `kubectl rollout restart deployment {service}`
2. Increase memory limits if justified
3. Profile application for leaks

## Monitoring

- Grafana Dashboard: https://grafana.internal/d/{service}
- Alerts: #{service}-alerts Slack channel
- Logs: `kubectl logs -l app={service} --tail=100`

## Contacts

- On-call: #{service}-oncall
- Team: #{service}-team
- Escalation: Platform Engineering

## Related Documents

- [[architecture-{service}|Architecture Overview]]
- [[deployment-{service}|Deployment Guide]]
'''

    return f"runbook-{service}.md", content


def generate_service_doc(service: str) -> tuple[str, str]:
    """Generate service documentation."""
    content = f'''---
title: "{service} Service"
tags: [service, {service}, documentation]
status: active
---

# {service}

## Purpose

The {service} handles core functionality for our platform.

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
kubectl apply -f k8s/{service}/
```

## Monitoring

- Metrics: Prometheus
- Logs: Azure Log Analytics
- Traces: Application Insights

## See Also

- [[runbook-{service}|Operational Runbook]]
- [[rca-{service}|Past Incidents]]
'''

    return f"{service}.md", content


def main():
    """Generate the sample vault."""
    vault_path = Path(__file__).parent.parent / "vault"

    # Create directories
    (vault_path / "RCAs").mkdir(parents=True, exist_ok=True)
    (vault_path / "Runbooks").mkdir(parents=True, exist_ok=True)
    (vault_path / "Services").mkdir(parents=True, exist_ok=True)

    base_date = datetime.now()

    # Generate RCAs (100 documents)
    print("Generating RCA documents...")
    for i in range(100):
        filename, content = generate_rca(i, base_date)
        filepath = vault_path / "RCAs" / filename

        # Avoid duplicates
        counter = 1
        while filepath.exists():
            name, ext = filename.rsplit('.', 1)
            filepath = vault_path / "RCAs" / f"{name}-{counter}.{ext}"
            counter += 1

        filepath.write_text(content)
        if (i + 1) % 20 == 0:
            print(f"  Generated {i + 1} RCAs...")

    # Generate runbooks
    print("Generating runbooks...")
    for service in SERVICES:
        filename, content = generate_runbook(service)
        (vault_path / "Runbooks" / filename).write_text(content)

    # Generate service docs
    print("Generating service documentation...")
    for service in SERVICES:
        filename, content = generate_service_doc(service)
        (vault_path / "Services" / filename).write_text(content)

    # Create vault README
    readme = f'''---
title: "DevOps Knowledge Base"
tags: [index, documentation]
---

# DevOps Knowledge Base

This vault contains operational documentation, RCA reports, and runbooks.

## Structure

- **RCAs/** - Root Cause Analysis reports for past incidents
- **Runbooks/** - Operational runbooks for each service  
- **Services/** - Service documentation and architecture

## Quick Links

### Services
{chr(10).join(f"- [[Services/{s}|{s}]]" for s in SERVICES)}

### Recent RCAs
See the RCAs folder for incident reports.

## Tags

- #rca - Root cause analyses
- #runbook - Operational runbooks
- #p1, #p2, #p3 - Severity levels
- #database, #infrastructure, #application - Issue categories

## Search Tips

Use semantic search to find related incidents:
- "database connection issues" - finds connection pool, timeout, deadlock issues
- "deployment failures" - finds rollback and deployment issues
- "kubernetes problems" - finds container and pod issues
'''

    (vault_path / "README.md").write_text(readme)

    print(f"\nVault generated at: {vault_path}")
    print(f"  - {len(list((vault_path / 'RCAs').glob('*.md')))} RCA documents")
    print(f"  - {len(list((vault_path / 'Runbooks').glob('*.md')))} Runbooks")
    print(f"  - {len(list((vault_path / 'Services').glob('*.md')))} Service docs")


if __name__ == "__main__":
    main()
