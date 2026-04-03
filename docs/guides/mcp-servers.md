# Manage MCP Servers

Use MCP management when you want one server definition shared across tools.

## List current central servers

```bash
damngood list
```

---

## Add a server

```bash
damngood add github
```

Editor template fields:

- `type` usually `stdio`
- `command` executable name
- `args` command arguments
- `env` environment variables
- `clients` client names to receive this server

Example:

```json
{
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_TOKEN": "${GITHUB_TOKEN}"
  },
  "clients": ["cursor", "claude", "opencode"]
}
```

---

## Edit / show / remove

```bash
damngood show github
damngood edit github
damngood remove github
```

---

## Sync to clients

```bash
damngood sync
```

Sync writes to each enabled client's configured MCP key (typically `mcpServers`).

---

## Import existing client MCP configs

```bash
damngood import
```

Import behavior:

- scans enabled clients
- prompts per discovered server
- stores imported entries in central registry

---

## Assignment strategy (recommended)

- keep `clients` explicit per server
- avoid assigning every server to every client by default
- use `damngood sync` after batched updates, not every single edit
