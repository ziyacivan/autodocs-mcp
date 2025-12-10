# autodocs-mcp

[![PyPI version](https://badge.fury.io/py/autodocs-mcp.svg)](https://badge.fury.io/py/autodocs-mcp)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![CI](https://github.com/ziyacivan/autodocs-mcp/workflows/CI/badge.svg)](https://github.com/ziyacivan/autodocs-mcp/actions)

Generate Model Context Protocol (MCP) servers from ReadTheDocs documentation.

## Overview

`autodocs-mcp` is a CLI tool that automatically scrapes ReadTheDocs documentation, generates embeddings for semantic search, and creates a ready-to-use MCP server that can be integrated with VSCode and other MCP-compatible tools.

## Features

- 🔍 **Format Detection**: Automatically detects documentation format (Sphinx, MkDocs, or generic)
- 📚 **Smart Scraping**: Uses `objects.inv` for Sphinx docs, `sitemap.xml` for MkDocs, with fallback to HTML crawling
- 🧠 **Semantic Search**: Generates embeddings and creates a vector store for semantic search
- ⚙️ **MCP Server Generation**: Creates a fully functional MCP server with tools and resources
- 🔌 **VSCode Integration**: Generates VSCode configuration for easy integration

## Installation

Install from [PyPI](https://pypi.org/project/autodocs-mcp/):

```bash
pip install autodocs-mcp
```

We recommend using [`uv`](https://github.com/astral-sh/uv) for faster and more reliable package management:

```bash
uv pip install autodocs-mcp
```

Or install from source:

```bash
git clone https://github.com/ziyacivan/autodocs-mcp.git
cd autodocs-mcp
uv sync
```

## Usage

After installation, you can use `autodocs-mcp` directly from the terminal:

### Basic Usage

```bash
autodocs-mcp generate https://docs.example.com/
```

Alternatively, you can run it as a Python module:

```bash
python -m autodocs_mcp generate https://docs.example.com/
```

### Options

```bash
autodocs-mcp generate <readthedocs_url> \
  --output-dir ./mcp-server \
  --embedding-model all-MiniLM-L6-v2 \
  --python-path python
```

**Options:**
- `--output-dir`: Output directory for generated files (default: `./mcp-server`)
- `--embedding-model`: Embedding model to use (default: `all-MiniLM-L6-v2`)
- `--cache-dir`: Cache directory (default: `output-dir/cache`)
- `--python-path`: Path to Python interpreter (default: `python`)

### Example

```bash
# Generate MCP server for a documentation site
autodocs-mcp generate https://docs.readthedocs.io/en/stable/

# This will:
# 1. Detect the documentation format
# 2. Scrape all pages
# 3. Generate embeddings
# 4. Create vector store
# 5. Generate MCP server code
# 6. Create VSCode configuration
```

## Output Structure

After running the tool, you'll get:

```
mcp-server/
├── mcp_server.py          # Generated MCP server
├── vector_store/          # ChromaDB vector store
├── vscode_config.json     # VSCode configuration
└── cache/                 # Cached content (optional)
```

## VSCode Integration

1. The tool generates a `vscode_config.json` file with the MCP server configuration.

2. Add the configuration to your VSCode `settings.json`:

```json
{
  "mcp.servers": {
    "docs-example-com": {
      "command": "python",
      "args": ["/path/to/mcp-server/mcp_server.py"]
    }
  }
}
```

3. Restart VSCode to load the MCP server.

## How It Works

### Format Detection

The tool automatically detects the documentation format:

1. **Sphinx**: Checks for `objects.inv` file
2. **MkDocs**: Checks for `sitemap.xml` file
3. **Generic**: Falls back to HTML crawling

### Scraping Process

- **Sphinx**: Uses `sphobjinv` to parse `objects.inv` and extract all documentation objects
- **MkDocs**: Parses `sitemap.xml` or analyzes HTML navigation structure
- **Generic**: Crawls HTML pages starting from the index page

### Embedding Generation

- Splits content into chunks (configurable size and overlap)
- Generates embeddings using sentence transformers
- Stores embeddings in ChromaDB vector store

### MCP Server Features

The generated MCP server provides:

- **Resources**: List of all documentation pages
- **Tools**:
  - `search_documentation`: Semantic search across documentation
  - `get_page_content`: Get full content of a specific page

## Requirements

- Python 3.10+
- See `pyproject.toml` for full dependency list

## Development

### Local Development Setup

For local development, install the package in editable mode:

```bash
# Clone the repository
git clone https://github.com/ziyacivan/autodocs-mcp.git
cd autodocs-mcp

# Install in editable mode with development dependencies
pip install -e ".[dev]"

# Or using uv
uv sync --extra dev
```

After installation, you can use the CLI tool:

```bash
# Using the CLI command (after editable install)
autodocs-mcp --help

# Or as a Python module
python -m autodocs_mcp --help
```

### Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=src/autodocs_mcp --cov-report=html

# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Fix auto-fixable linting issues
ruff check --fix src/ tests/

# Install pre-commit hooks (optional but recommended)
pre-commit install
```

## License

MIT License - see LICENSE file for details.

## Troubleshooting

### Common Issues

**Issue: "No pages found"**
- Ensure the URL is correct and accessible
- Check if the documentation site requires authentication
- Verify the site is using a supported format (Sphinx, MkDocs, or generic HTML)

**Issue: "Could not find Python executable"**
- Specify the Python path explicitly using `--python-path`
- Ensure Python 3.10+ is installed and in your PATH

**Issue: Embedding model download fails**
- Check your internet connection
- The model will be downloaded on first use from Hugging Face
- Ensure you have sufficient disk space (~100MB per model)

**Issue: MCP server not working in VSCode**
- Verify the Python path in `vscode_config.json` is correct
- Ensure all dependencies are installed: `uv pip install chromadb sentence-transformers mcp` (or `pip install chromadb sentence-transformers mcp`)
- Check VSCode MCP extension is installed and enabled
- Restart VSCode after configuration changes

### Performance Tips

- Use a smaller embedding model (e.g., `all-MiniLM-L6-v2`) for faster processing
- Enable caching to avoid re-scraping documentation
- For large documentation sites, consider processing in batches

## Roadmap

- [ ] Support for additional documentation formats
- [ ] Incremental updates (only scrape changed pages)
- [ ] Custom chunking strategies
- [ ] Multiple embedding model support
- [ ] Docker containerization
- [ ] Pre-built MCP servers for popular documentation sites

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Model Context Protocol](https://modelcontextprotocol.io/)
- Uses [ChromaDB](https://www.trychroma.com/) for vector storage
- Powered by [Sentence Transformers](https://www.sbert.net/)
