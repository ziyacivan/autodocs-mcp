# Contributing to autodocs-mcp

Thank you for your interest in contributing to autodocs-mcp! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the issue list to see if the bug has already been reported. When creating a bug report, include:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)
- Any relevant error messages or logs

Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md) when creating an issue.

### Suggesting Features

Feature requests are welcome! Please provide:

- A clear description of the feature
- Use cases and motivation
- Potential implementation approach (if you have ideas)

Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md) when creating an issue.

### Pull Requests

1. **Fork the repository** and create your branch from `master`
2. **Make your changes** following our coding standards
3. **Add tests** for new functionality
4. **Update documentation** as needed
5. **Ensure all tests pass** and code is properly formatted
6. **Submit a pull request** with a clear description

#### Pull Request Process

1. Update the CHANGELOG.md with your changes
2. Ensure your code follows the style guidelines (run `black` and `ruff`)
3. Add tests for new code
4. Ensure all tests pass (`pytest`)
5. Update documentation if needed
6. Request review from maintainers

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- [`uv`](https://github.com/astral-sh/uv) (recommended) or `pip`

### Setup Steps

1. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/autodocs-mcp.git
   cd autodocs-mcp
   ```

2. Install dependencies using `uv` (recommended):
   ```bash
   # uv automatically creates and manages virtual environment
   uv sync --extra dev
   ```

   Or using `pip`:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. Install pre-commit hooks (optional but recommended):
   ```bash
   pre-commit install
   ```

## Coding Standards

### Code Style

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use `black` for code formatting (line length: 100)
- Use `ruff` for linting
- Maximum line length: 100 characters

### Formatting and Linting

Before committing, run:

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Fix auto-fixable issues
ruff check --fix src/ tests/
```

### Type Hints

- Use type hints for all function signatures
- Use `typing` module for complex types
- Prefer `|` syntax for unions (Python 3.10+)

### Docstrings

- Use Google-style docstrings
- Include descriptions for all public functions and classes
- Document parameters, return values, and exceptions

Example:
```python
def example_function(param1: str, param2: int) -> bool:
    """
    Brief description of the function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is empty
    """
    pass
```

### Testing

- Write tests for all new features
- Aim for good test coverage
- Use descriptive test names
- Follow the existing test structure

Run tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=src/autodocs_mcp --cov-report=html
```

## Project Structure

```
autodocs-mcp/
├── src/
│   └── autodocs_mcp/
│       ├── cli.py              # CLI entry point
│       ├── embedding/         # Embedding generation
│       ├── mcp/               # MCP server generation
│       ├── scraper/           # Documentation scraping
│       └── vscode/            # VSCode configuration
├── tests/                      # Test files
├── .github/                    # GitHub templates and workflows
└── docs/                       # Additional documentation
```

## Commit Messages

- Use clear, descriptive commit messages
- Start with a verb in imperative mood (e.g., "Add", "Fix", "Update")
- Reference issue numbers when applicable: "Fix #123: ..."

Examples:
- `Add support for custom embedding models`
- `Fix URL normalization in scraper`
- `Update README with troubleshooting section`

## Questions?

If you have questions about contributing, feel free to:

- Open an issue with the `question` label
- Check existing issues and discussions
- Review the documentation

Thank you for contributing to autodocs-mcp!
