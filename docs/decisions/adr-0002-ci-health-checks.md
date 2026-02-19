---
status: accepted
date: 2026-01-29
---

# CI Health Checks as Quality Gates

## Context

We need automated quality enforcement that runs on every PR. The goal is to catch issues before merge without requiring manual review for every change.

## Decision Drivers

- **Trust the gates**: CI should be reliable enough to merge without manual review when green
- **Fast feedback**: Developers should know within minutes if something's broken
- **Comprehensive**: Cover formatting, linting, type safety, security, and tests
- **Multi-version**: Support Python 3.11 and 3.12

## Decision

Implement two GitHub Actions workflows:

1. **Code Quality Checks** (fast, <1 min)
   - Black formatting verification
   - Ruff linting
   - Bandit security scanning
   - MyPy type checking

2. **Test Suite** (parallel matrix)
   - pytest on Python 3.11
   - pytest on Python 3.12

All checks must pass before merge. Branch protection enforces this.

## Implementation

```yaml
# Runs on: push to main, all PRs
jobs:
  code-quality:  # Single job, sequential checks
  tests:         # Matrix: [3.11, 3.12]
```

Pre-commit hooks run the same checks locally, catching issues before push.

## Consequences

**Good:**
- Consistent code style enforced automatically
- Security issues caught early (bandit)
- Type errors don't reach main
- Multi-version compatibility verified

**Bad:**
- CI time adds to PR cycle (~2 min total)
- Developers must run formatters locally (or pre-commit does it)

**Acceptable because:**
- 2 minutes is negligible for the safety gained
- Pre-commit hooks make local compliance easy

## Notes

May add code coverage requirements later. Current focus is on establishing the pattern.
