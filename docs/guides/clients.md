# Manage Clients

Clients represent target tools where DamnGood writes config.

## List clients

```bash
damngood client list
```

This includes:

- auto-discovered clients
- custom registered clients
- enabled/disabled status

---

## Enable or disable a client

```bash
damngood client enable cursor
damngood client disable gemini
```

Disabled clients are skipped during sync.

---

## Register a custom client

```bash
damngood client register mytool --path ~/.mytool/config.json --key mcpServers
```

Parameters:

- `name`: client identifier
- `--path`: target JSON config path
- `--key`: JSON key for MCP servers

---

## Remove a custom client

```bash
damngood client remove mytool
```

Auto-discovered clients cannot be removed; disable them instead.

---

## Recommended client policy

- keep all active tools enabled
- disable tools you are not currently using
- assign servers/snippets/skills explicitly with `clients`
