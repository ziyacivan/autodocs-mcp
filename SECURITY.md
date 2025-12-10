# Security Policy

## Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability, please follow these steps:

1. **Do not** open a public GitHub issue
2. Email the maintainer directly at [security@example.com] or create a [security advisory](https://github.com/ziyacivan/autodocs-mcp/security/advisories/new) with details about the vulnerability
3. Include the following information:
   - Type of vulnerability
   - Full paths of source file(s) related to the vulnerability
   - Location of the affected source code (tag/branch/commit or direct URL)
   - Step-by-step instructions to reproduce the issue
   - Proof-of-concept or exploit code (if possible)
   - Impact of the issue, including how an attacker might exploit the issue

### What to Expect

- You will receive an acknowledgment within 48 hours
- We will provide an initial assessment within 7 days
- We will keep you informed of the progress toward a fix
- We will notify you when the vulnerability is fixed

### Disclosure Policy

- We will work with you to understand and resolve the issue quickly
- Security vulnerabilities will be disclosed publicly after a fix is available
- Credit will be given to the reporter (unless they prefer to remain anonymous)

## Security Best Practices

When using autodocs-mcp, please follow these security best practices:

1. **Keep dependencies updated**: Regularly update all dependencies to receive security patches
2. **Validate URLs**: Only use trusted documentation sources
3. **Review generated code**: Always review generated MCP server code before deployment
4. **Use virtual environments**: Isolate dependencies using virtual environments
5. **Limit network access**: If scraping from untrusted sources, consider network isolation
6. **Monitor resource usage**: Be aware of disk space usage for vector stores and cache

## Known Security Considerations

- **Network requests**: The tool makes HTTP requests to documentation sites. Ensure you trust the source.
- **File system access**: The tool creates files and directories. Ensure output directories are secure.
- **Model downloads**: Embedding models are downloaded from Hugging Face. Verify model integrity if needed.
- **Generated code execution**: Generated MCP servers execute Python code. Review generated code before use.

## Security Updates

Security updates will be released as patch versions (e.g., 0.1.1, 0.1.2) and will be documented in the CHANGELOG.md file.

Thank you for helping keep autodocs-mcp and its users safe!
