"""
Command-line interface for Obsidian RAG.
"""

import json

import click
from dotenv import load_dotenv

# Load .env file
load_dotenv()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Obsidian RAG - Semantic search for your vault."""
    pass


@cli.command()
@click.argument("vault_path", type=click.Path(exists=True))
@click.option("--force", "-f", is_flag=True, help="Force reindex all files")
@click.option(
    "--persist-dir", "-p", default=".chroma", help="ChromaDB storage directory"
)
def index(vault_path: str, force: bool, persist_dir: str):
    """Index an Obsidian vault for semantic search."""
    from src.rag import RAGEngine

    click.echo(f"Indexing vault: {vault_path}")

    engine = RAGEngine(
        vault_path=vault_path,
        persist_dir=persist_dir,
    )

    stats = engine.index(force=force)

    click.echo("\nIndex complete:")
    click.echo(f"  Files: {stats.total_files}")
    click.echo(f"  Chunks: {stats.total_chunks}")
    click.echo(f"  Indexed at: {stats.indexed_at}")


def validate_top_k(ctx, param, value):
    """Validate top_k is within acceptable bounds."""
    if value < 1:
        raise click.BadParameter("must be at least 1")
    if value > 50:
        raise click.BadParameter("cannot exceed 50")
    return value


@cli.command()
@click.argument("query")
@click.option(
    "--vault",
    "-v",
    envvar="OBSIDIAN_VAULT_PATH",
    required=True,
    help="Path to Obsidian vault",
)
@click.option(
    "--persist-dir", "-p", default=".chroma", help="ChromaDB storage directory"
)
@click.option(
    "--top-k",
    "-k",
    default=5,
    callback=validate_top_k,
    help="Number of results to return (1-50)",
)
@click.option("--tags", "-t", multiple=True, help="Filter by tags")
@click.option("--json-output", "-j", is_flag=True, help="Output as JSON")
def search(
    query: str, vault: str, persist_dir: str, top_k: int, tags: tuple, json_output: bool
):
    """Search the vault semantically."""
    # Validate query is not empty
    if not query or not query.strip():
        raise click.UsageError("Query cannot be empty")

    from src.rag import RAGEngine

    engine = RAGEngine(
        vault_path=vault,
        persist_dir=persist_dir,
    )

    tag_list = list(tags) if tags else None
    response = engine.search(query, top_k=top_k, tags=tag_list)

    if json_output:
        click.echo(json.dumps(response.to_dict(), indent=2))
        return

    click.echo(f"Query: {query}")
    n_results = len(response.results)
    n_searched = response.total_chunks_searched
    click.echo(f"Found {n_results} results (searched {n_searched} chunks)\n")

    for i, result in enumerate(response.results, 1):
        click.echo(f"--- Result {i} (score: {result.score:.3f}) ---")
        click.echo(f"Source: {result.source_path}")
        if result.heading:
            click.echo(f"Section: {result.heading}")
        if result.tags:
            click.echo(f"Tags: {', '.join(result.tags)}")
        click.echo(f"\n{result.content[:500]}...")
        click.echo()


@cli.command()
@click.option(
    "--vault",
    "-v",
    envvar="OBSIDIAN_VAULT_PATH",
    required=True,
    help="Path to Obsidian vault",
)
@click.option(
    "--persist-dir", "-p", default=".chroma", help="ChromaDB storage directory"
)
def stats(vault: str, persist_dir: str):
    """Show index statistics."""
    from src.rag import RAGEngine

    engine = RAGEngine(
        vault_path=vault,
        persist_dir=persist_dir,
    )

    index_stats = engine.get_stats()

    click.echo(f"Vault: {index_stats.vault_path}")
    click.echo(f"Files: {index_stats.total_files}")
    click.echo(f"Chunks indexed: {index_stats.total_chunks}")


@cli.command()
@click.option(
    "--vault",
    "-v",
    envvar="OBSIDIAN_VAULT_PATH",
    required=True,
    help="Path to Obsidian vault",
)
@click.option(
    "--persist-dir", "-p", default=".chroma", help="ChromaDB storage directory"
)
def serve(vault: str, persist_dir: str):
    """Start the MCP server (stdio transport)."""
    from src.mcp.server import run_server

    # Log to stderr to avoid interfering with MCP JSON-RPC on stdout
    click.echo(f"Starting MCP server for vault: {vault}", err=True)
    click.echo(f"ChromaDB: {persist_dir}", err=True)
    click.echo("Using stdio transport (for Claude Code integration)", err=True)

    run_server(
        vault_path=vault,
        persist_dir=persist_dir,
    )


if __name__ == "__main__":
    cli()
