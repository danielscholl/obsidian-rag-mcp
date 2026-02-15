"""
MCP Server for Obsidian RAG.

Exposes semantic search and vault operations as MCP tools.
"""

import json
import logging
import os
from typing import Any

from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolResult,
    TextContent,
    Tool,
)

from mcp.server import Server
from obsidian_rag_mcp.rag import RAGEngine

logger = logging.getLogger(__name__)

# Validation constants
MIN_TOP_K = 1
MAX_TOP_K = 50
MIN_LIMIT = 1
MAX_LIMIT = 100
MAX_QUERY_LENGTH = 10000


# Global engine instance (initialized on server start)
_engine: RAGEngine | None = None


def get_engine() -> RAGEngine:
    """Get the RAG engine instance."""
    if _engine is None:
        raise RuntimeError("RAG engine not initialized. Call run_server() first.")
    return _engine


def validate_top_k(value: Any, default: int = 5) -> int:
    """Validate and clamp top_k parameter."""
    if value is None:
        return default
    try:
        k = int(value)
        return max(MIN_TOP_K, min(k, MAX_TOP_K))
    except (TypeError, ValueError):
        return default


def validate_limit(value: Any, default: int = 10) -> int:
    """Validate and clamp limit parameter."""
    if value is None:
        return default
    try:
        lim = int(value)
        return max(MIN_LIMIT, min(lim, MAX_LIMIT))
    except (TypeError, ValueError):
        return default


def validate_query(value: str) -> str:
    """Validate and sanitize query string."""
    if not value or not isinstance(value, str):
        raise ValueError("Query must be a non-empty string")
    # Truncate overly long queries
    if len(value) > MAX_QUERY_LENGTH:
        logger.warning(f"Query truncated from {len(value)} to {MAX_QUERY_LENGTH} chars")
        value = value[:MAX_QUERY_LENGTH]
    return value.strip()


def validate_path(value: str) -> str:
    """Validate path string."""
    if not value or not isinstance(value, str):
        raise ValueError("Path must be a non-empty string")
    # Basic sanitization - strip whitespace
    return value.strip()


def validate_tags(value: Any) -> list[str]:
    """Validate tags array."""
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError("Tags must be an array")
    # Ensure all tags are strings and non-empty
    return [str(t).strip() for t in value if t and str(t).strip()]


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
                    "description": "Natural language search query",
                },
                "top_k": {
                    "type": "integer",
                    "description": f"Number of results to return (1-{MAX_TOP_K}, default: 5)",
                    "default": 5,
                    "minimum": MIN_TOP_K,
                    "maximum": MAX_TOP_K,
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional: filter by tags (e.g., ['rca', 'billing'])",
                },
            },
            "required": ["query"],
        },
    ),
    Tool(
        name="search_by_tag",
        description=(
            "Search for documents with specific tags. Useful when you know the "
            "category but want to explore related content. "
            "If no query is provided, tags are used as the semantic search query."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Tags to search for (OR logic)",
                },
                "query": {
                    "type": "string",
                    "description": (
                        "Optional: semantic query to rank results. "
                        "If omitted, tags are used as the query."
                    ),
                },
                "top_k": {
                    "type": "integer",
                    "description": f"Number of results to return (1-{MAX_TOP_K}, default: 5)",
                    "default": 5,
                    "minimum": MIN_TOP_K,
                    "maximum": MAX_TOP_K,
                },
            },
            "required": ["tags"],
        },
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
                    "description": "Relative path to the note (e.g., 'RCAs/incident.md')",
                }
            },
            "required": ["path"],
        },
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
                "path": {"type": "string", "description": "Path to the source note"},
                "top_k": {
                    "type": "integer",
                    "description": f"Number of related notes to return (1-{MAX_TOP_K}, default: 5)",
                    "default": 5,
                    "minimum": MIN_TOP_K,
                    "maximum": MAX_TOP_K,
                },
            },
            "required": ["path"],
        },
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
                    "description": f"Number of notes to return (1-{MAX_LIMIT}, default: 10)",
                    "default": 10,
                    "minimum": MIN_LIMIT,
                    "maximum": MAX_LIMIT,
                }
            },
        },
    ),
    Tool(
        name="index_status",
        description=(
            "Check the status of the search index. Shows number of files "
            "indexed and other statistics."
        ),
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="search_with_reasoning",
        description=(
            "Search the vault with reasoning layer. Returns relevant document chunks "
            "PLUS logical conclusions extracted from the content. Use this when you need "
            "not just raw text but synthesized insights and patterns. Only available when "
            "reasoning is enabled during indexing."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Natural language search query",
                },
                "top_k": {
                    "type": "integer",
                    "description": f"Number of results to return (1-{MAX_TOP_K}, default: 5)",
                    "default": 5,
                    "minimum": MIN_TOP_K,
                    "maximum": MAX_TOP_K,
                },
                "conclusion_types": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["deductive", "inductive", "abductive"],
                    },
                    "description": "Filter conclusions by type (default: all types)",
                },
                "min_confidence": {
                    "type": "number",
                    "description": "Minimum confidence for conclusions (0-1, default: 0)",
                    "default": 0,
                    "minimum": 0,
                    "maximum": 1,
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional: filter by tags",
                },
            },
            "required": ["query"],
        },
    ),
    Tool(
        name="get_conclusion_trace",
        description=(
            "Get the reasoning trace for a specific conclusion. Shows the evidence chain: "
            "source chunk -> conclusion -> related conclusions. Use this to understand "
            "WHY a conclusion was drawn and what evidence supports it."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "conclusion_id": {
                    "type": "string",
                    "description": "ID of the conclusion to trace",
                },
                "max_depth": {
                    "type": "integer",
                    "description": "Maximum depth for finding related conclusions (default: 3)",
                    "default": 3,
                    "minimum": 1,
                    "maximum": 10,
                },
            },
            "required": ["conclusion_id"],
        },
    ),
    Tool(
        name="explore_connected_conclusions",
        description=(
            "Explore conclusions related to a query or another conclusion. Use this to "
            "discover what else the system knows about a topic or find connections "
            "between different pieces of knowledge."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Text query to find related conclusions",
                },
                "conclusion_id": {
                    "type": "string",
                    "description": "ID of conclusion to find related ones (alternative to query)",
                },
                "top_k": {
                    "type": "integer",
                    "description": f"Maximum conclusions to return (1-{MAX_TOP_K}, default: 10)",
                    "default": 10,
                    "minimum": MIN_TOP_K,
                    "maximum": MAX_TOP_K,
                },
                "min_confidence": {
                    "type": "number",
                    "description": "Minimum confidence threshold (0-1, default: 0)",
                    "default": 0,
                    "minimum": 0,
                    "maximum": 1,
                },
            },
        },
    ),
]


async def handle_tool_call(name: str, arguments: dict[str, Any]) -> CallToolResult:
    """Handle a tool call from MCP client."""
    engine = get_engine()

    try:
        if name == "search_vault":
            query = validate_query(arguments["query"])
            top_k = validate_top_k(arguments.get("top_k"))
            tags = validate_tags(arguments.get("tags"))

            logger.info(
                f"search_vault: query='{query[:50]}...', top_k={top_k}, tags={tags}"
            )

            response = engine.search(
                query=query,
                top_k=top_k,
                tags=tags if tags else None,
            )
            return CallToolResult(
                content=[
                    TextContent(
                        type="text", text=json.dumps(response.to_dict(), indent=2)
                    )
                ]
            )

        elif name == "search_by_tag":
            tags = validate_tags(arguments.get("tags"))
            if not tags:
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text", text="Error: At least one tag is required"
                        )
                    ],
                    isError=True,
                )

            top_k = validate_top_k(arguments.get("top_k"))
            query = arguments.get("query", "")
            if query:
                query = validate_query(query)
            else:
                # If no query, use tags as semantic search
                query = " ".join(tags)
                logger.info(f"No query provided, using tags as query: {query}")

            logger.info(f"search_by_tag: tags={tags}, top_k={top_k}")

            response = engine.search(
                query=query,
                top_k=top_k,
                tags=tags,
            )
            return CallToolResult(
                content=[
                    TextContent(
                        type="text", text=json.dumps(response.to_dict(), indent=2)
                    )
                ]
            )

        elif name == "get_note":
            path = validate_path(arguments["path"])

            logger.info(f"get_note: path='{path}'")

            content = engine.get_note(path)
            if content is None:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Note not found: {path}")],
                    isError=True,
                )
            return CallToolResult(content=[TextContent(type="text", text=content)])

        elif name == "get_related":
            path = validate_path(arguments["path"])
            top_k = validate_top_k(arguments.get("top_k"))

            logger.info(f"get_related: path='{path}', top_k={top_k}")

            response = engine.get_related(
                path=path,
                top_k=top_k,
            )
            return CallToolResult(
                content=[
                    TextContent(
                        type="text", text=json.dumps(response.to_dict(), indent=2)
                    )
                ]
            )

        elif name == "list_recent":
            limit = validate_limit(arguments.get("limit"))

            logger.info(f"list_recent: limit={limit}")

            recent = engine.list_recent(limit=limit)
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(recent, indent=2))]
            )

        elif name == "index_status":
            logger.info("index_status")

            stats = engine.get_stats()
            return CallToolResult(
                content=[
                    TextContent(type="text", text=json.dumps(stats.to_dict(), indent=2))
                ]
            )

        elif name == "search_with_reasoning":
            query = validate_query(arguments["query"])
            top_k = validate_top_k(arguments.get("top_k"))
            tags = validate_tags(arguments.get("tags"))
            conclusion_types = arguments.get("conclusion_types")
            min_confidence = arguments.get("min_confidence", 0.0)

            # Validate conclusion_types
            if conclusion_types is not None:
                if not isinstance(conclusion_types, list):
                    conclusion_types = [conclusion_types]
                valid_types = {"deductive", "inductive", "abductive"}
                conclusion_types = [t for t in conclusion_types if t in valid_types]

            # Validate min_confidence
            try:
                min_confidence = float(min_confidence)
                min_confidence = max(0.0, min(1.0, min_confidence))
            except (TypeError, ValueError):
                min_confidence = 0.0

            logger.info(
                f"search_with_reasoning: query='{query[:50]}...', top_k={top_k}, "
                f"types={conclusion_types}, min_conf={min_confidence}"
            )

            response = engine.search_with_reasoning(
                query=query,
                top_k=top_k,
                conclusion_types=conclusion_types if conclusion_types else None,
                min_confidence=min_confidence,
                tags=tags if tags else None,
            )
            return CallToolResult(
                content=[
                    TextContent(
                        type="text", text=json.dumps(response.to_dict(), indent=2)
                    )
                ]
            )

        elif name == "get_conclusion_trace":
            conclusion_id = arguments.get("conclusion_id")
            if not conclusion_id:
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text", text="Error: conclusion_id is required"
                        )
                    ],
                    isError=True,
                )

            max_depth = arguments.get("max_depth", 3)
            try:
                max_depth = int(max_depth)
                max_depth = max(1, min(10, max_depth))
            except (TypeError, ValueError):
                max_depth = 3

            logger.info(
                f"get_conclusion_trace: id='{conclusion_id[:20]}...', depth={max_depth}"
            )

            trace = engine.get_conclusion_trace(
                conclusion_id=conclusion_id,
                max_depth=max_depth,
            )

            if trace is None:
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=f"Conclusion not found: {conclusion_id}",
                        )
                    ],
                    isError=True,
                )

            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(trace, indent=2))]
            )

        elif name == "explore_connected_conclusions":
            query = arguments.get("query")
            conclusion_id = arguments.get("conclusion_id")

            if not query and not conclusion_id:
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text="Error: Either query or conclusion_id is required",
                        )
                    ],
                    isError=True,
                )

            top_k = validate_top_k(arguments.get("top_k"), default=10)

            min_confidence = arguments.get("min_confidence", 0.0)
            try:
                min_confidence = float(min_confidence)
                min_confidence = max(0.0, min(1.0, min_confidence))
            except (TypeError, ValueError):
                min_confidence = 0.0

            if query:
                query = validate_query(query)

            logger.info(
                f"explore_connected_conclusions: query='{query[:30] if query else None}', "
                f"id='{conclusion_id[:20] if conclusion_id else None}', top_k={top_k}"
            )

            connected = engine.explore_connected_conclusions(
                query=query,
                conclusion_id=conclusion_id,
                top_k=top_k,
                min_confidence=min_confidence,
            )

            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(connected, indent=2))]
            )

        else:
            logger.warning(f"Unknown tool: {name}")
            return CallToolResult(
                content=[TextContent(type="text", text=f"Unknown tool: {name}")],
                isError=True,
            )

    except ValueError as e:
        logger.warning(f"Validation error in {name}: {e}")
        return CallToolResult(
            content=[TextContent(type="text", text=f"Validation error: {str(e)}")],
            isError=True,
        )

    except Exception as e:
        logger.exception(f"Error in {name}: {e}")
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error: {str(e)}")], isError=True
        )


def run_server(
    vault_path: str,
    persist_dir: str = ".vault",
    reasoning_enabled: bool = False,
):
    """
    Run the MCP server.

    Args:
        vault_path: Path to the Obsidian vault
        persist_dir: ChromaDB storage directory
        reasoning_enabled: Enable reasoning layer for conclusion extraction
    """
    global _engine

    logger.info("Starting Obsidian RAG MCP server")
    logger.info(f"Vault path: {vault_path}")
    logger.info(f"Persist dir: {persist_dir}")
    logger.info(f"Reasoning enabled: {reasoning_enabled}")

    # Initialize the RAG engine
    _engine = RAGEngine(
        vault_path=vault_path,
        persist_dir=persist_dir,
        reasoning_enabled=reasoning_enabled,
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

    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream, write_stream, server.create_initialization_options()
            )

    asyncio.run(run())


def main():
    """Entry point for MCP server."""
    # Configure logging to stderr (stdout is reserved for MCP JSON-RPC)
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stderr,
    )

    vault_path = os.getenv("OBSIDIAN_VAULT_PATH", "./vault")
    persist_dir = os.getenv("CHROMA_PERSIST_DIR", ".vault")
    reasoning_enabled = os.getenv("REASONING_ENABLED", "false").lower() in (
        "true",
        "1",
        "yes",
    )

    run_server(vault_path, persist_dir, reasoning_enabled=reasoning_enabled)


if __name__ == "__main__":
    main()
