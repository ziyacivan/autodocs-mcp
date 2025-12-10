"""Tests for VSCode configuration module."""

import pytest
import json
from pathlib import Path
from autodocs_mcp.vscode import generate_vscode_config, save_vscode_config


def test_generate_vscode_config():
    """Test generating VSCode configuration."""
    config = generate_vscode_config(
        server_name="test-server",
        server_path="/path/to/server.py",
        python_path="/usr/bin/python3",
    )
    
    assert "mcp.servers" in config
    assert "test-server" in config["mcp.servers"]
    assert config["mcp.servers"]["test-server"]["command"] == "/usr/bin/python3"
    assert config["mcp.servers"]["test-server"]["args"] == ["/path/to/server.py"]


def test_save_vscode_config(tmp_path):
    """Test saving VSCode configuration to file."""
    config_path = tmp_path / "vscode_config.json"
    
    save_vscode_config(
        config_path=str(config_path),
        server_name="test-server",
        server_path="/path/to/server.py",
        python_path="/usr/bin/python3",
    )
    
    assert config_path.exists()
    
    with open(config_path) as f:
        config = json.load(f)
    
    assert "mcp.servers" in config
    assert "test-server" in config["mcp.servers"]
