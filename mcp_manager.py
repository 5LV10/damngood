#!/usr/bin/env python3
"""
Damn Good MCP Server Manager
A simple tool to manage multiple MCP (Model Context Protocol) servers
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

# Default MCP config paths (supports various MCP clients)
DEFAULT_CONFIG_PATHS = [
    # Cursor
    Path.home() / ".cursor" / "mcp.json",  # Cursor global
    Path.cwd() / ".cursor" / "mcp.json",  # Cursor project-level
    Path.home()
    / "Library"
    / "Application Support"
    / "Cursor"
    / "cursor_desktop_config.json",  # Cursor macOS
    # Gemini CLI
    Path.home() / ".gemini" / "settings.json",  # Gemini CLI global
    Path.cwd() / ".gemini" / "settings.json",  # Gemini CLI project-level
    # OpenCode
    Path.home() / ".config" / "opencode" / "opencode.json",  # OpenCode global
    Path.home() / ".config" / "opencode" / "mcp.json",  # OpenCode MCP only
    Path.cwd() / "opencode.json",  # OpenCode project-level
    Path.cwd() / ".opencode" / "opencode.json",  # OpenCode project alternative
    # Claude
    Path.home() / ".claude" / "config.json",  # Claude Code
    Path.home() / ".config" / "claude" / "config.json",  # Claude Desktop
    Path.home()
    / "Library"
    / "Application Support"
    / "Claude"
    / "claude_desktop_config.json",  # Claude Desktop macOS
    Path.cwd() / ".claude" / "config.json",  # Project-level Claude Code
    # Generic MCP
    Path.home() / ".mcp" / "config.json",
    Path.home() / ".config" / "mcp" / "config.json",  # XDG standard
    Path.cwd() / "mcp_config.json",  # Project-level generic
]


class MCPServerManager:
    # Client types and their MCP config keys
    CLIENT_FORMATS = {
        "opencode": "mcp",
        "cursor": "mcpServers",
        "gemini": "mcpServers",
        "claude": "mcpServers",
        "generic": "mcpServers",
    }

    # Default config paths for each client type
    CLIENT_PATHS = {
        "cursor": Path.home() / ".cursor" / "mcp.json",
        "gemini": Path.home() / ".gemini" / "settings.json",
        "opencode": Path.home() / ".config" / "opencode" / "opencode.json",
        "claude": Path.home() / ".claude" / "config.json",
        "generic": Path.home() / ".mcp" / "config.json",
    }

    def __init__(
        self, config_path: Optional[str] = None, client_type: Optional[str] = None
    ):
        # Priority: 1) explicit config_path, 2) explicit client_type, 3) auto-detect
        if config_path:
            # User specified exact path
            self.config_path = Path(config_path)
            self.client_type = self._detect_client_type()
        elif client_type:
            # User specified which client to use - ignore any existing configs
            self.client_type = client_type.lower()
            self.config_path = self.CLIENT_PATHS.get(
                self.client_type, self.CLIENT_PATHS["generic"]
            )
        else:
            # Auto-detect from existing configs
            self.config_path = self._find_config()
            self.client_type = self._detect_client_type()
        self.config = self._load_config()

    def _detect_client_type(self) -> str:
        """Detect which MCP client this config belongs to"""
        path_str = str(self.config_path).lower()
        if "opencode" in path_str:
            return "opencode"
        elif "cursor" in path_str:
            return "cursor"
        elif "gemini" in path_str:
            return "gemini"
        elif "claude" in path_str:
            return "claude"
        return "generic"

    def _get_mcp_key(self) -> str:
        """Get the MCP config key for the current client"""
        return self.CLIENT_FORMATS.get(self.client_type, "mcpServers")

    def _find_config(self) -> Path:
        """Find the MCP config file in standard locations"""
        for path in DEFAULT_CONFIG_PATHS:
            if path.exists():
                return path
        return DEFAULT_CONFIG_PATHS[0]

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if not self.config_path.exists():
            return {self._get_mcp_key(): {}}
        try:
            with open(self.config_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {self.config_path}")
            sys.exit(1)

    def save(self):
        """Save configuration to file"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=2)
        print(f"Config saved to {self.config_path} ({self.client_type} format)")

    def list_servers(self):
        """List all configured MCP servers"""
        mcp_key = self._get_mcp_key()
        servers = self.config.get(mcp_key, {})
        if not servers:
            print("No MCP servers configured.")
            return

        print(f"\nConfigured MCP Servers ({self.client_type}):")
        print("-" * 60)
        for name, config in servers.items():
            status = "enabled" if config.get("enabled", True) else "disabled"
            print(f"  {name:<20} [{status}]")
            print(f"    Type: {config.get('type', 'stdio')}")
            print(f"    Command: {config.get('command', 'N/A')}")
            print()

    def add_server(
        self,
        name: str,
        command: str,
        args: Optional[List[str]] = None,
        env: Optional[Dict[str, str]] = None,
        server_type: str = "stdio",
    ):
        """Add a new MCP server"""
        mcp_key = self._get_mcp_key()
        if mcp_key not in self.config:
            self.config[mcp_key] = {}

        self.config[mcp_key][name] = {
            "type": server_type,
            "command": command,
            "args": args or [],
            "env": env or {},
            "enabled": True,
        }
        print(f"Added MCP server: {name}")

    def remove_server(self, name: str):
        """Remove an MCP server"""
        mcp_key = self._get_mcp_key()
        if name in self.config.get(mcp_key, {}):
            del self.config[mcp_key][name]
            print(f"Removed MCP server: {name}")
        else:
            print(f"Server not found: {name}")
            sys.exit(1)

    def toggle_server(self, name: str, enabled: Optional[bool] = None):
        """Enable or disable an MCP server"""
        mcp_key = self._get_mcp_key()
        servers = self.config.get(mcp_key, {})
        if name not in servers:
            print(f"Server not found: {name}")
            sys.exit(1)

        if enabled is None:
            enabled = not servers[name].get("enabled", True)

        servers[name]["enabled"] = enabled
        status = "enabled" if enabled else "disabled"
        print(f"Server '{name}' {status}")

    def get_server(self, name: str) -> Dict[str, Any]:
        """Get server configuration"""
        mcp_key = self._get_mcp_key()
        return self.config.get(mcp_key, {}).get(name, {})

    def export_config(self, output_path: str):
        """Export configuration to a new file"""
        output = Path(output_path)
        with open(output, "w") as f:
            json.dump(self.config, f, indent=2)
        print(f"Config exported to {output}")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Damn Good MCP Server Manager - Supports Cursor, Gemini CLI, OpenCode, Claude, and generic MCP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Supported Clients: cursor, gemini, opencode, claude, generic
Config Auto-Detection: ~/.cursor/mcp.json, ~/.gemini/settings.json, ~/.config/opencode/opencode.json, etc.

Examples:
  %(prog)s list                                   # Auto-detect client
  %(prog)s --client cursor list                   # Explicitly use Cursor
  %(prog)s --client opencode add myserver --command npx
  %(prog)s --config ~/.cursor/mcp.json list       # Use specific config file
        """,
    )
    parser.add_argument("--config", "-c", help="Path to config file")
    parser.add_argument(
        "--client",
        choices=["cursor", "gemini", "opencode", "claude", "generic"],
        help="Specify which MCP client to use (takes precedence over auto-detection)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # List command
    list_parser = subparsers.add_parser("list", help="List all MCP servers")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new MCP server")
    add_parser.add_argument("name", help="Server name")
    add_parser.add_argument("--command", "-cmd", required=True, help="Command to run")
    add_parser.add_argument("--args", "-a", nargs="*", help="Arguments")
    add_parser.add_argument(
        "--env", "-e", nargs="*", help="Environment variables (KEY=VALUE)"
    )
    add_parser.add_argument(
        "--type", default="stdio", help="Server type (default: stdio)"
    )

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove an MCP server")
    remove_parser.add_argument("name", help="Server name")

    # Enable/Disable commands
    enable_parser = subparsers.add_parser("enable", help="Enable an MCP server")
    enable_parser.add_argument("name", help="Server name")

    disable_parser = subparsers.add_parser("disable", help="Disable an MCP server")
    disable_parser.add_argument("name", help="Server name")

    # Toggle command
    toggle_parser = subparsers.add_parser("toggle", help="Toggle an MCP server")
    toggle_parser.add_argument("name", help="Server name")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export config to file")
    export_parser.add_argument("path", help="Output file path")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    manager = MCPServerManager(args.config, args.client)

    if args.command == "list":
        manager.list_servers()

    elif args.command == "add":
        env_dict = {}
        if args.env:
            for env_var in args.env:
                key, value = env_var.split("=", 1)
                env_dict[key] = value
        manager.add_server(args.name, args.command, args.args, env_dict, args.type)
        manager.save()

    elif args.command == "remove":
        manager.remove_server(args.name)
        manager.save()

    elif args.command == "enable":
        manager.toggle_server(args.name, True)
        manager.save()

    elif args.command == "disable":
        manager.toggle_server(args.name, False)
        manager.save()

    elif args.command == "toggle":
        manager.toggle_server(args.name)
        manager.save()

    elif args.command == "export":
        manager.export_config(args.path)


if __name__ == "__main__":
    main()
