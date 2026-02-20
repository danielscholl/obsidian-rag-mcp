# Contributing to obsidian-rag-mcp

Thank you for your interest in contributing! This guide will help you get started.

## Development Setup

```bash
# Clone
git clone https://github.com/danielscholl/obsidian-rag-mcp.git
cd obsidian-rag-mcp

# Install dependencies (using uv)
uv sync

# Install pre-commit hooks
uv run pre-commit install
```

See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for Windows instructions.

## Development Workflow

1. Create a feature branch from `main`: `git checkout -b feat/your-feature`
2. Make changes
3. Run quality checks (see below)
4. Commit using [Conventional Commits](#commit-messages)
5. Push and open a Pull Request against `main`
6. Wait for CI + code review
7. Merge when approved

## Quality Checks

Run all checks before committing:

```bash
# Format
uv run black obsidian_rag_mcp/ tests/

# Lint
uv run ruff check obsidian_rag_mcp/ tests/

# Type check
uv run mypy obsidian_rag_mcp/

# Tests with coverage
uv run pytest --cov=obsidian_rag_mcp --cov-fail-under=50

# Security scan
uv run bandit -r obsidian_rag_mcp/ -ll -x tests/
```

## Code Standards

- **Formatting**: `black` (line length 100 via ruff, black defaults)
- **Linting**: `ruff` with rules E, F, I, N, W, UP
- **Type checking**: `mypy --strict`
- **Type hints**: Required for all public functions
- **Tests**: Required for new features; minimum 50% coverage

## Commit Messages

This project uses [Conventional Commits](https://www.conventionalcommits.org/) to enable automated releases via Release Please.

### Format

```
<type>(<optional scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | When to use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `test` | Adding or updating tests |
| `chore` | Maintenance (CI, deps, config) |
| `perf` | Performance improvement |

### Examples

```
feat: add tag-based search filtering
fix: handle empty vault gracefully during indexing
docs: add Azure OpenAI configuration guide
refactor(rag): simplify chunker boundary detection
test: add integration tests for reasoning extractor
chore(ci): add CodeQL security scanning
```

**Breaking changes**: Add `!` after the type or include `BREAKING CHANGE:` in the footer:

```
feat!: require Python 3.12+
```

## Testing

```bash
# All tests
uv run pytest

# Specific file
uv run pytest tests/test_engine.py

# With coverage report
uv run pytest --cov=obsidian_rag_mcp --cov-report=html
open htmlcov/index.html
```

## Pull Request Process

1. Fill out the PR template
2. Ensure CI passes (lint, test, type-check)
3. Link related issues (`Fixes #123`)
4. Keep PRs focused -- one logical change per PR
5. Update documentation if your change affects user-facing behavior
6. Add tests for new functionality

## Documentation

- Update relevant docs when changing functionality
- Keep README.md current
- Add ADRs for significant architectural decisions (`docs/decisions/`)

## Security

If you discover a security vulnerability, please report it via
[GitHub Security Advisories](https://github.com/danielscholl/obsidian-rag-mcp/security/advisories/new)
rather than opening a public issue.
