# Contributing to obsidian-rag-mcp

## Development Setup

1. Clone the repo
2. Create a virtual environment: `python -m venv .venv`
3. Install dependencies: `pip install -e ".[dev]"`
4. Install pre-commit hooks: `pre-commit install`

## Workflow

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes
3. Run tests: `pytest tests/ -v`
4. Run linting: `black src/ tests/ && ruff check src/ tests/`
5. Commit and push
6. Open a Pull Request
7. Wait for CI + Copilot review
8. Merge when approved

## Code Standards

- Format with `black`
- Lint with `ruff`
- Type hints required
- Tests required for new features
- Security scans must pass (`bandit`)

## Private Project

This is private work. Do not publish to PyPI or share externally.
