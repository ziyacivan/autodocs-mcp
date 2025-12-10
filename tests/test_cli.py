"""Tests for CLI module."""

from click.testing import CliRunner
from autodocs_mcp.cli import cli, find_python_executable


def test_cli_help():
    """Test CLI help command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "autodocs-mcp" in result.output


def test_cli_generate_help():
    """Test generate command help."""
    runner = CliRunner()
    result = runner.invoke(cli, ["generate", "--help"])
    assert result.exit_code == 0
    assert "Generate an MCP server" in result.output


def test_cli_generate_invalid_url():
    """Test generate command with invalid URL."""
    runner = CliRunner()
    result = runner.invoke(cli, ["generate", "not-a-url"])
    assert result.exit_code == 1
    assert "Invalid URL" in result.output


def test_find_python_executable():
    """Test finding Python executable."""
    python_path = find_python_executable()
    assert python_path is not None
    assert "python" in python_path.lower()


def test_cli_generate_missing_url():
    """Test generate command without URL."""
    runner = CliRunner()
    result = runner.invoke(cli, ["generate"])
    assert result.exit_code != 0
