# Config Files

## Central DamnGood directory

```text
~/.damngood/
  registry.json
  clients.json
  instructions/
    index.json
    <name>.md
  skills/
    index.json
    <name>/
      content.md
```

---

## `registry.json` (MCP source of truth)

Example:

```json
{
  "servers": {
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem"],
      "env": {},
      "clients": ["cursor", "gemini"],
      "created_at": "2026-04-03T11:22:33.000000",
      "updated_at": "2026-04-03T11:22:33.000000"
    }
  }
}
```

---

## `clients.json`

Example:

```json
{
  "clients": {
    "cursor": {
      "name": "cursor",
      "path": "/home/user/.cursor/mcp.json",
      "key": "mcpServers",
      "auto_discovered": true,
      "enabled": true
    }
  }
}
```

---

## `instructions/index.json`

Tracks snippet metadata:

- description
- assigned clients
- enabled state
- timestamps

The snippet body lives in `instructions/<name>.md`.

---

## `skills/index.json`

Tracks skill metadata:

- description
- `user_invocable`
- `allowed_tools`
- assigned clients
- enabled state
- timestamps

Skill body lives in `skills/<name>/content.md`.
