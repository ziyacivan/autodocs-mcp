"""Tests for MCP server generation module."""

from autodocs_mcp.mcp import generate_mcp_server


def test_generate_mcp_server(tmp_path):
    """Test generating MCP server code."""
    output_path = tmp_path / "mcp_server.py"
    vector_store_path = tmp_path / "vector_store"
    vector_store_path.mkdir()

    generate_mcp_server(
        output_path=str(output_path),
        vector_store_path=str(vector_store_path),
        embedding_model="all-MiniLM-L6-v2",
        documentation_url="https://docs.example.com/",
        collection_name="documentation",
    )

    assert output_path.exists()

    # Check that generated file contains expected content
    content = output_path.read_text()
    assert "mcp" in content.lower() or "MCP" in content
    assert "all-MiniLM-L6-v2" in content or "embedding" in content.lower()
