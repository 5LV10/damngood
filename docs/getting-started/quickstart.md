# Quickstart (10 Minutes)

This guide gets you to a working multi-client setup fast.

## 1) See detected clients

```bash
damngood client list
```

Expected outcome:

- installed clients show as `enabled`
- each client includes its config path

---

## 2) Import existing MCP configs

```bash
damngood import
```

DamnGood checks enabled clients and offers to import discovered servers into the central registry.

Registry file:

- `~/.damngood/registry.json`

---

## 3) Add one MCP server centrally

```bash
damngood add filesystem
```

Your editor opens with a template JSON. Example:

```json
{
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem"],
  "env": {},
  "clients": ["cursor", "gemini", "opencode"]
}
```

Sync to all assigned clients:

```bash
damngood sync
```

---

## 4) Add and sync instructions

```bash
damngood instructions add coding-style
damngood instructions sync
```

Starter snippet:

```markdown
---
description: "Shared coding defaults"
clients: [claude, gemini, cursor, windsurf, opencode, continue]
enabled: true
---

Prefer small, focused functions.
Add tests when fixing bugs.
Explain non-obvious trade-offs in code comments.
```

---

## 5) Add and sync one skill

```bash
damngood skills add review-pr
damngood skills sync
```

Starter skill:

```markdown
---
description: "Review a PR for correctness and risk"
user-invocable: true
allowed-tools: [Read, Grep, Bash]
clients: [claude, opencode]
enabled: true
---

# review-pr

Review the proposed changes and report:
1. correctness issues
2. security risks
3. missing tests
4. migration or rollback risk
```

---

## 6) Confirm results

Run these commands:

```bash
damngood list
damngood instructions list
damngood skills list
```

You now have one source of truth for MCP, instructions, and skills.
