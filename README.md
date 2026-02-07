# DamnGood MCP Manager

A simple CLI tool to manage Model Context Protocol (MCP) servers across multiple AI coding assistants.

## Supported Clients

- **Cursor** - `~/.cursor/mcp.json`
- **Claude** (Code & Desktop) - `~/.claude/config.json`
- **Gemini CLI** - `~/.gemini/settings.json`
- **OpenCode** - `~/.config/opencode/opencode.json`
- **Generic MCP** - `~/.mcp/config.json`
- **Custom Tools** - Register any MCP-compatible tool

## Quick Start

```bash
# List servers (auto-detects client)
python3 mcp_manager.py list

# Add a server
python3 mcp_manager.py add filesystem --command npx --args "-y @modelcontextprotocol/server-filesystem"

# Toggle server on/off
python3 mcp_manager.py toggle filesystem

# Remove a server
python3 mcp_manager.py remove filesystem
```

## Usage

```
python3 mcp_manager.py [options] <command>

Commands:
  list              List all configured servers
  add <name>        Add a new MCP server
  remove <name>     Remove a server
  enable <name>     Enable a server
  disable <name>    Disable a server
  toggle <name>     Toggle server state
  export <path>     Export config to file
  register <name>   Register a custom MCP client

Options:
  -c, --config      Specify custom config file path
  --client          Specify which client to use (cursor/gemini/opencode/claude/generic)
```

## Specify Your Client

By default, the tool auto-detects which MCP client you're using based on existing config files. But you can explicitly specify:

```bash
# Use Cursor explicitly (ignores other configs)
python3 mcp_manager.py --client cursor list

# Use Gemini explicitly
python3 mcp_manager.py --client gemini add myserver --command npx

# Use OpenCode explicitly
python3 mcp_manager.py --client opencode enable myserver
```

This is useful when you have multiple MCP configs but want to manage a specific one.

## Register Custom Tools

Want to use a tool that's not in our supported list? Register it:

```bash
# Register a custom tool (e.g., VS Code)
python3 mcp_manager.py register windsurf --path ~/.windsurf/mcp.json

# Register with custom config key (like OpenCode uses 'mcp' instead of 'mcpServers')
python3 mcp_manager.py register mytool --path ~/.mytool/config.json --key mcp

# Now use it like any other client
python3 mcp_manager.py --client windsurf list
python3 mcp_manager.py --client windsurf add myserver --command npx
```

Custom tools are saved to `~/.config/damngood/custom_tools.json` and work exactly like built-in ones.

## Why Use This?

- **No manual JSON editing** - Simple CLI commands
- **Works everywhere** - Auto-detects Cursor, Claude, Gemini, OpenCode
- **Explicit control** - Use `--client` to force a specific tool
- **Extensible** - Register any MCP-compatible tool
- **Safe** - Can't break your config with typos
- **Fast** - Enable/disable servers in seconds

## Examples

### Auto-detection workflow
```bash
# Your Cursor MCP servers are acting up
$ python3 mcp_manager.py list
Configured MCP Servers (cursor):
------------------------------------------------------------
  filesystem           [enabled]
  slack                [enabled]
  postgres             [enabled]

# Disable the broken one
$ python3 mcp_manager.py disable slack
Server 'slack' disabled
Config saved to /home/dev/.cursor/mcp.json (cursor format)
```

### Explicit client selection
```bash
# Force use of Claude even if other configs exist
$ python3 mcp_manager.py --client claude list
Configured MCP Servers (claude):
------------------------------------------------------------
No MCP servers configured.

# Add server to Claude specifically
$ python3 mcp_manager.py --client claude add github --command npx --args "-y @modelcontextprotocol/server-github"
Added MCP server: github
Config saved to /home/dev/.claude/config.json (claude format)
```

### Custom tool registration
```bash
# Register VS Code as custom tool
$ python3 mcp_manager.py register vscode --path ~/.vscode/mcp.json
Registered custom tool 'vscode' -> /home/dev/.vscode/mcp.json (key: mcpServers)

# Use it
$ python3 mcp_manager.py --client vscode list
Configured MCP Servers (vscode):
------------------------------------------------------------
  myserver             [enabled]
```

## Install

```bash
git clone <repo>
cd damngood
python3 mcp_manager.py --help
```

## Config Locations

The tool searches for configs in this order:
1. `~/.cursor/mcp.json` (Cursor)
2. `~/.gemini/settings.json` (Gemini CLI)
3. `~/.config/opencode/opencode.json` (OpenCode)
4. `~/.claude/config.json` (Claude)
5. `~/.mcp/config.json` (Generic)

Project-level configs are also checked (e.g., `./.cursor/mcp.json`).

Use `--config <path>` to specify an exact file, or `--client <name>` to use a specific client's default location.
