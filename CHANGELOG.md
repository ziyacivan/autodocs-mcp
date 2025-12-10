# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial open-source release preparation
- Comprehensive documentation (CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md)
- GitHub issue and pull request templates
- CI/CD workflows for testing and linting
- Test infrastructure setup

## [0.1.1] - 2025-01-XX

### Fixed
- Fixed format detection to use GET requests when HEAD fails (some servers don't support HEAD)
- Increased timeouts from 10s to 30-60s for better reliability on slow connections
- Improved error handling and logging throughout the scraping process
- Enhanced generic scraper with ReadTheDocs-specific navigation selectors
- Added fallback mechanism when format-specific scraping fails
- Better error messages when no pages are found
- Fixed issue where process would hang without proper error reporting

### Improved
- Better progress indicators and error messages in CLI
- More robust format detection with HTML content analysis
- Enhanced generic scraper to find navigation links in common ReadTheDocs locations
- Added redirect following support throughout the codebase

## [0.1.0] - 2025-01-XX

### Added
- Initial release
- CLI tool for generating MCP servers from ReadTheDocs documentation
- Support for Sphinx documentation format detection and scraping
- Support for MkDocs documentation format detection and scraping
- Generic HTML fallback scraper
- Embedding generation using sentence transformers
- ChromaDB vector store integration
- MCP server code generation
- VSCode configuration generation
- Format detection (Sphinx, MkDocs, generic)
- Semantic search capabilities
- Page content retrieval tools

### Features
- Automatic documentation format detection
- Smart scraping using `objects.inv` (Sphinx) and `sitemap.xml` (MkDocs)
- Configurable embedding models
- Vector store persistence
- Generated MCP server with search and content retrieval tools
- VSCode integration support

[Unreleased]: https://github.com/ziyacivan/autodocs-mcp/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/ziyacivan/autodocs-mcp/releases/tag/v0.1.0



