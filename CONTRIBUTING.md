# Contributing to obsidian-rag-mcp

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

## Workflow

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes
3. Run tests: `uv run pytest`
4. Run linting: `uv run black obsidian_rag_mcp/ tests/ && uv run ruff check obsidian_rag_mcp/ tests/`
5. Commit and push
6. Open a Pull Request
7. Wait for CI + Claude review
8. Merge when approved

## Code Standards

- Format with `black`
- Lint with `ruff`
- Type hints encouraged
- Tests required for new features
- 88 tests currently passing

## Testing

```bash
# All tests
uv run pytest

# Specific file
uv run pytest tests/test_engine.py

# With coverage
uv run pytest --cov=obsidian_rag_mcp
```

## Documentation

- Update relevant docs when changing functionality
- Keep README.md current
- Add ADRs for significant decisions (`docs/decisions/`)
