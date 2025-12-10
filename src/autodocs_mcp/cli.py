"""CLI entry point for autodocs-mcp."""

import asyncio
import sys
import shutil
from pathlib import Path
from urllib.parse import urlparse

import click

from .scraper import ReadTheDocsScraper
from .embedding import EmbeddingGenerator, VectorStore
from .mcp import generate_mcp_server
from .vscode import save_vscode_config


@click.group()
def cli():
    """autodocs-mcp: Generate MCP servers from ReadTheDocs documentation."""
    pass


@cli.command()
@click.argument("readthedocs_url", type=str)
@click.option(
    "--output-dir",
    type=click.Path(file_okay=False, dir_okay=True),
    default="./mcp-server",
    help="Output directory for generated files",
)
@click.option(
    "--embedding-model",
    type=str,
    default="all-MiniLM-L6-v2",
    help="Embedding model to use",
)
@click.option(
    "--cache-dir",
    type=click.Path(file_okay=False, dir_okay=True),
    default=None,
    help="Cache directory (default: output-dir/cache)",
)
@click.option(
    "--python-path",
    type=str,
    default=None,
    help="Path to Python interpreter for MCP server (auto-detected if not specified)",
)
def generate(
    readthedocs_url: str,
    output_dir: str,
    embedding_model: str,
    cache_dir: str | None,
    python_path: str | None,
):
    """
    Generate an MCP server from ReadTheDocs documentation.

    READTHEDOCS_URL: URL of the ReadTheDocs documentation (e.g., https://docs.example.com/)
    """
    # Validate URL
    parsed = urlparse(readthedocs_url)
    if not parsed.scheme or not parsed.netloc:
        click.echo(f"Error: Invalid URL: {readthedocs_url}", err=True)
        sys.exit(1)

    # Normalize URL
    if not readthedocs_url.endswith("/"):
        readthedocs_url = readthedocs_url + "/"

    # Auto-detect Python path if not specified
    if python_path is None:
        python_path = find_python_executable()
        if python_path is None:
            click.echo(
                "Error: Could not find Python executable. Please specify --python-path", err=True
            )
            sys.exit(1)

    # Setup paths
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if cache_dir is None:
        cache_dir = str(output_path / "cache")
    cache_path = Path(cache_dir)
    cache_path.mkdir(parents=True, exist_ok=True)

    # Run async main
    asyncio.run(
        async_main(
            readthedocs_url,
            output_path,
            cache_path,
            embedding_model,
            python_path,
        )
    )


def find_python_executable() -> str | None:
    """Find Python executable, preferring python3 over python."""
    # Try python3 first
    python3_path = shutil.which("python3")
    if python3_path:
        return python3_path

    # Fallback to python
    python_path = shutil.which("python")
    if python_path:
        return python_path

    # Try sys.executable (current Python)
    if sys.executable:
        return sys.executable

    return None


async def async_main(
    readthedocs_url: str,
    output_path: Path,
    cache_path: Path,
    embedding_model: str,
    python_path: str,
):
    """Async main function."""
    click.echo(f"🚀 Starting MCP server generation for: {readthedocs_url}")
    click.echo(f"📁 Output directory: {output_path}")

    # Step 1: Scrape documentation
    click.echo("\n📚 Step 1: Scraping documentation...")
    try:
        async with ReadTheDocsScraper(readthedocs_url) as scraper:
            click.echo("   Detecting documentation format...")
            pages = await scraper.detect_and_scrape()
            click.echo(f"   Found {len(pages)} pages")

            if not pages:
                click.echo("❌ Error: No pages found. Please check the URL.", err=True)
                click.echo(f"   Tried URL: {readthedocs_url}", err=True)
                click.echo("   Possible issues:", err=True)
                click.echo("   - URL might be incorrect or inaccessible", err=True)
                click.echo("   - Documentation might require authentication", err=True)
                click.echo("   - Network connection issues", err=True)
                sys.exit(1)

            # Fetch content
            click.echo("   Fetching page content...")
            pages_with_content = await scraper.fetch_all_content(pages, progress=True)
            click.echo(f"   Successfully fetched {len(pages_with_content)} pages")

            if not pages_with_content:
                click.echo("❌ Error: Failed to fetch any page content.", err=True)
                sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Error during scraping: {e}", err=True)
        import traceback

        click.echo(traceback.format_exc(), err=True)
        sys.exit(1)

    # Step 2: Generate embeddings
    click.echo("\n🔢 Step 2: Generating embeddings...")
    try:
        generator = EmbeddingGenerator(model_name=embedding_model)
        chunks = generator.process_pages(pages_with_content)
        click.echo(f"   Generated {len(chunks)} chunks")
    except Exception as e:
        click.echo(f"❌ Error during embedding generation: {e}", err=True)
        import traceback

        click.echo(traceback.format_exc(), err=True)
        sys.exit(1)

    # Step 3: Store in vector database
    click.echo("\n💾 Step 3: Storing in vector database...")
    try:
        vector_store_path = output_path / "vector_store"
        store = VectorStore(
            persist_directory=str(vector_store_path),
            collection_name="documentation",
        )
        store.add_chunks(chunks)
        click.echo(f"   Stored {len(chunks)} chunks in vector store")
    except Exception as e:
        click.echo(f"❌ Error during vector store creation: {e}", err=True)
        import traceback

        click.echo(traceback.format_exc(), err=True)
        sys.exit(1)

    # Step 4: Generate MCP server
    click.echo("\n⚙️  Step 4: Generating MCP server...")
    try:
        server_path = output_path / "mcp_server.py"
        generate_mcp_server(
            output_path=str(server_path),
            vector_store_path=str(vector_store_path),
            embedding_model=embedding_model,
            documentation_url=readthedocs_url,
            collection_name="documentation",
        )
        click.echo(f"   Generated MCP server: {server_path}")
    except Exception as e:
        click.echo(f"❌ Error during MCP server generation: {e}", err=True)
        import traceback

        click.echo(traceback.format_exc(), err=True)
        sys.exit(1)

    # Step 5: Generate VSCode config
    click.echo("\n🔧 Step 5: Generating VSCode configuration...")
    try:
        server_name = urlparse(readthedocs_url).netloc.replace(".", "-")
        config_path = output_path / "vscode_config.json"
        save_vscode_config(
            config_path=str(config_path),
            server_name=server_name,
            server_path=str(server_path.absolute()),
            python_path=python_path,
        )
        click.echo(f"   Generated VSCode config: {config_path}")
    except Exception as e:
        click.echo(f"❌ Error during VSCode config generation: {e}", err=True)
        import traceback

        click.echo(traceback.format_exc(), err=True)
        sys.exit(1)

    # Final instructions
    click.echo("\n✅ Generation complete!")
    click.echo("\n📋 Next steps:")
    click.echo("   1. Add the following to your VSCode settings.json:")
    with open(config_path) as f:
        config_content = f.read()
        click.echo(f"      {config_content}")
    click.echo("\n   2. Or manually add:")
    click.echo('      "mcp.servers": {')
    click.echo(f'        "{server_name}": {{')
    click.echo(f'          "command": "{python_path}",')
    click.echo(f'          "args": ["{server_path.absolute()}"]')
    click.echo("        }")
    click.echo("      }")
    click.echo("\n   3. Restart VSCode to load the MCP server")


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
