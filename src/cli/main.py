"""
Command-line interface for Obsidian RAG.
"""

import json
import os
from pathlib import Path

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
@click.option("--persist-dir", "-p", default=".chroma", help="ChromaDB storage directory")
def index(vault_path: str, force: bool, persist_dir: str):
    """Index an Obsidian vault for semantic search."""
    from src.rag import RAGEngine
    
    click.echo(f"Indexing vault: {vault_path}")
    
    engine = RAGEngine(
        vault_path=vault_path,
        persist_dir=persist_dir,
    )
    
    stats = engine.index(force=force)
    
    click.echo(f"\nIndex complete:")
    click.echo(f"  Files: {stats.total_files}")
    click.echo(f"  Chunks: {stats.total_chunks}")
    click.echo(f"  Indexed at: {stats.indexed_at}")


@cli.command()
@click.argument("query")
@click.option("--vault", "-v", envvar="OBSIDIAN_VAULT_PATH", required=True,
              help="Path to Obsidian vault")
@click.option("--persist-dir", "-p", default=".chroma", help="ChromaDB storage directory")
@click.option("--top-k", "-k", default=5, help="Number of results to return")
@click.option("--tags", "-t", multiple=True, help="Filter by tags")
@click.option("--json-output", "-j", is_flag=True, help="Output as JSON")
def search(query: str, vault: str, persist_dir: str, top_k: int, tags: tuple, json_output: bool):
    """Search the vault semantically."""
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
    click.echo(f"Found {len(response.results)} results (searched {response.total_chunks_searched} chunks)\n")
    
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
@click.option("--vault", "-v", envvar="OBSIDIAN_VAULT_PATH", required=True,
              help="Path to Obsidian vault")
@click.option("--persist-dir", "-p", default=".chroma", help="ChromaDB storage directory")
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
@click.option("--vault", "-v", envvar="OBSIDIAN_VAULT_PATH", required=True,
              help="Path to Obsidian vault")
@click.option("--persist-dir", "-p", default=".chroma", help="ChromaDB storage directory")
@click.option("--host", default="localhost", help="Server host")
@click.option("--port", default=8765, help="Server port")
def serve(vault: str, persist_dir: str, host: str, port: int):
    """Start the MCP server."""
    from src.mcp.server import run_server
    
    click.echo(f"Starting MCP server for vault: {vault}")
    click.echo(f"ChromaDB: {persist_dir}")
    
    run_server(
        vault_path=vault,
        persist_dir=persist_dir,
    )


if __name__ == "__main__":
    cli()
