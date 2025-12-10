"""VSCode MCP server configuration generator."""

import json
from pathlib import Path
from typing import Dict


def generate_vscode_config(
    server_name: str,
    server_path: str,
    python_path: str = "python",
) -> Dict:
    """
    Generate VSCode MCP server configuration.

    Args:
        server_name: Name of the MCP server
        server_path: Path to the MCP server script
        python_path: Path to Python interpreter

    Returns:
        Dictionary with VSCode configuration
    """
    config = {
        "mcp.servers": {
            server_name: {
                "command": python_path,
                "args": [server_path],
            }
        }
    }

    return config


def save_vscode_config(
    config_path: str,
    server_name: str,
    server_path: str,
    python_path: str = "python",
) -> str:
    """
    Save VSCode configuration to a file.

    Args:
        config_path: Path to save the config file
        server_name: Name of the MCP server
        server_path: Path to the MCP server script
        python_path: Path to Python interpreter

    Returns:
        Path to the saved config file
    """
    config = generate_vscode_config(server_name, server_path, python_path)

    config_path_obj = Path(config_path)
    config_path_obj.parent.mkdir(parents=True, exist_ok=True)

    # Write JSON config
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    return str(config_path)
