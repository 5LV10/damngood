# DamnGood MCP Manager

A simple CLI tool to manage Model Context Protocol (MCP) servers across multiple AI coding assistants.

## Supported Clients

- **Cursor** - `~/.cursor/mcp.json`
- **Claude** (Code & Desktop) - `~/.claude/config.json`
- **Gemini CLI** - `~/.gemini/settings.json`
- **OpenCode** - `~/.config/opencode/opencode.json`
- **Generic MCP** - `~/.mcp/config.json`

## Quick Start

```bash
# List servers
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

Options:
  -c, --config      Specify custom config file path
```

## Why Use This?

- **No manual JSON editing** - Simple CLI commands
- **Works everywhere** - Auto-detects Cursor, Claude, Gemini, OpenCode
- **Safe** - Can't break your config with typos
- **Fast** - Enable/disable servers in seconds

## Example

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

## Install

```bash
git clone <repo>
cd damngood
python3 mcp_manager.py --help
```
