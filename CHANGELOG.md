# Changelog

## [0.1.0](https://github.com/danielscholl/obsidian-rag-mcp/releases/tag/v0.1.0) (2025-06-01)

### Features

* MCP server with semantic search over Obsidian vaults
* CLI for indexing and querying (`obsidian-rag index`, `obsidian-rag search`)
* ChromaDB-backed vector store (local, no external database)
* OpenAI and Azure OpenAI embedding support
* Intelligent markdown chunking (respects headers, code blocks, front-matter)
* Tag-based filtering (`search_by_tag`)
* Related-note discovery (`get_related`)
* Reasoning/conclusion extraction for enriched search results
* CI pipeline with black, ruff, bandit, pip-audit, and pytest
