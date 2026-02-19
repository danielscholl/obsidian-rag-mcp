# Support

## Getting Help

- **Documentation** -- See the [README](README.md) and the [docs/](docs/) folder
- **Bug Reports** -- Open a [GitHub Issue](https://github.com/danielscholl/obsidian-rag-mcp/issues/new?template=bug-report.yml)
- **Feature Requests** -- Open a [GitHub Issue](https://github.com/danielscholl/obsidian-rag-mcp/issues/new?template=feature-request.yml)
- **Questions** -- Use [GitHub Discussions](https://github.com/danielscholl/obsidian-rag-mcp/discussions) or open an issue

## Common Issues

| Problem | Solution |
|---------|----------|
| `OPENAI_API_KEY` not set | Export the variable or add it to `.env` |
| ChromaDB permission errors | Ensure `.chroma/` is writable |
| Import errors after install | Run `uv sync` to install all dependencies |
| Tests failing locally | Run `uv run pytest -v` for verbose output |

## Security Issues

If you discover a security vulnerability, please report it responsibly via
[GitHub Security Advisories](https://github.com/danielscholl/obsidian-rag-mcp/security/advisories/new)
rather than opening a public issue.
