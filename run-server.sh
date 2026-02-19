#!/bin/bash
# MCP Server launcher for Claude Code integration

cd "$(dirname "$0")"
source .venv/bin/activate

# Load environment
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Default vault path if not set
export OBSIDIAN_VAULT_PATH="${OBSIDIAN_VAULT_PATH:-./vault}"
export PYTHONPATH="${PYTHONPATH:-.}"

exec python -m obsidian_rag_mcp.mcp.server "$@"
