# How DamnGood Works

DamnGood runs in a **centralized registry model**.

You define configuration once, then push it to client-native files.

## Central data model

All source-of-truth files live under:

```text
~/.damngood/
```

Main stores:

- `registry.json` for MCP servers
- `instructions/index.json` + markdown files for snippets
- `skills/index.json` + markdown files for skill content
- `clients.json` for client state and enable/disable flags

---

## Sync model

Every feature follows the same pattern:

1. read central registry
2. filter by `enabled` and `clients` assignment
3. write to each target client's native path

Examples:

- MCP servers -> `mcpServers` in client JSON config
- instructions -> managed block in client instruction file
- skills -> managed `SKILL.md` files in client skills directory

---

## Client capability awareness

Not every client supports every feature.

DamnGood has a capability matrix and only syncs compatible data types:

- instructions-only clients receive instruction snippets
- skills-capable clients receive skills
- MCP-compatible clients receive server definitions

This keeps sync predictable and avoids invalid writes.

---

## Why this approach is fast for onboarding

- one command per area (`sync`, `instructions sync`, `skills sync`)
- explicit client assignment per item
- no manual drift across multiple files and tools
- easy to inspect and version control central markdown/json content
