"""
MCP Server for Obsidian RAG.

Exposes semantic search and vault operations as MCP tools.
"""

import json
import os
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolResult,
    TextContent,
    Tool,
)

from src.rag import RAGEngine


# Global engine instance (initialized on server start)
_engine: RAGEngine | None = None


def get_engine() -> RAGEngine:
    """Get the RAG engine instance."""
    if _engine is None:
        raise RuntimeError("RAG engine not initialized. Call run_server() first.")
    return _engine


# Define MCP tools
TOOLS = [
    Tool(
        name="search_vault",
        description=(
            "Search the Obsidian vault semantically. Returns relevant document chunks "
            "based on meaning, not just keyword matching. Use this to find information "
            "about specific topics, past incidents, or documentation."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Natural language search query"
                },
                "top_k": {
                    "type": "integer",
                    "description": "Number of results to return (default: 5)",
                    "default": 5
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional: filter by tags (e.g., ['rca', 'billing'])"
                }
            },
            "required": ["query"]
        }
    ),
    Tool(
        name="search_by_tag",
        description=(
            "Search for documents with specific tags. Useful when you know the "
            "category but want to explore related content."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Tags to search for (OR logic)"
                },
                "query": {
                    "type": "string",
                    "description": "Optional: additional semantic query to rank results"
                },
                "top_k": {
                    "type": "integer",
                    "description": "Number of results to return (default: 5)",
                    "default": 5
                }
            },
            "required": ["tags"]
        }
    ),
    Tool(
        name="get_note",
        description=(
            "Get the full content of a specific note by its path. "
            "Use this when you need the complete document, not just a snippet."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path to the note (e.g., 'RCAs/2024-01-15-database-outage.md')"
                }
            },
            "required": ["path"]
        }
    ),
    Tool(
        name="get_related",
        description=(
            "Find notes related to a given note. Useful for discovering "
            "connected information or similar past incidents."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the source note"
                },
                "top_k": {
                    "type": "integer",
                    "description": "Number of related notes to return (default: 5)",
                    "default": 5
                }
            },
            "required": ["path"]
        }
    ),
    Tool(
        name="list_recent",
        description=(
            "List recently modified notes in the vault. "
            "Useful for finding recent RCAs or documentation updates."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Number of notes to return (default: 10)",
                    "default": 10
                }
            }
        }
    ),
    Tool(
        name="index_status",
        description=(
            "Check the status of the search index. Shows number of files "
            "indexed and other statistics."
        ),
        inputSchema={
            "type": "object",
            "properties": {}
        }
    ),
]


async def handle_tool_call(name: str, arguments: dict[str, Any]) -> CallToolResult:
    """Handle a tool call from MCP client."""
    engine = get_engine()
    
    try:
        if name == "search_vault":
            response = engine.search(
                query=arguments["query"],
                top_k=arguments.get("top_k", 5),
                tags=arguments.get("tags"),
            )
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(response.to_dict(), indent=2)
                )]
            )
        
        elif name == "search_by_tag":
            query = arguments.get("query", "")
            if not query:
                # If no query, use a generic one
                query = " ".join(arguments["tags"])
            
            response = engine.search(
                query=query,
                top_k=arguments.get("top_k", 5),
                tags=arguments["tags"],
            )
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(response.to_dict(), indent=2)
                )]
            )
        
        elif name == "get_note":
            content = engine.get_note(arguments["path"])
            if content is None:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"Note not found: {arguments['path']}"
                    )],
                    isError=True
                )
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=content
                )]
            )
        
        elif name == "get_related":
            response = engine.get_related(
                path=arguments["path"],
                top_k=arguments.get("top_k", 5),
            )
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(response.to_dict(), indent=2)
                )]
            )
        
        elif name == "list_recent":
            recent = engine.list_recent(limit=arguments.get("limit", 10))
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(recent, indent=2)
                )]
            )
        
        elif name == "index_status":
            stats = engine.get_stats()
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(stats.to_dict(), indent=2)
                )]
            )
        
        else:
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Unknown tool: {name}"
                )],
                isError=True
            )
    
    except Exception as e:
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )],
            isError=True
        )


def run_server(
    vault_path: str,
    persist_dir: str = ".chroma",
):
    """
    Run the MCP server.
    
    Args:
        vault_path: Path to the Obsidian vault
        persist_dir: ChromaDB storage directory
    """
    global _engine
    
    # Initialize the RAG engine
    _engine = RAGEngine(
        vault_path=vault_path,
        persist_dir=persist_dir,
    )
    
    # Create MCP server
    server = Server("obsidian-rag")
    
    @server.list_tools()
    async def list_tools():
        return TOOLS
    
    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]):
        return await handle_tool_call(name, arguments)
    
    # Run the server over stdio
    import asyncio
    asyncio.run(stdio_server(server))


if __name__ == "__main__":
    import sys
    
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH", "./vault")
    persist_dir = os.getenv("CHROMA_PERSIST_DIR", ".chroma")
    
    run_server(vault_path, persist_dir)
