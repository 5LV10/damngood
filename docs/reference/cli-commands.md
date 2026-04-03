# CLI Commands

This reference reflects current CLI behavior.

## Global usage

```bash
damngood [--config PATH] [--client CLIENT] <command>
```

Main commands:

- `list`
- `add <name>`
- `edit <name>`
- `remove <name>`
- `show <name>`
- `sync`
- `import`
- `instructions ...`
- `skills ...`
- `client ...`

Legacy single-client commands are also available (`enable`, `disable`, `toggle`, `export`, `register`).

---

## MCP commands (central mode)

```bash
damngood list
damngood add <name>
damngood edit <name>
damngood remove <name>
damngood show <name>
damngood sync
damngood import
```

---

## Instructions commands

```bash
damngood instructions list
damngood instructions add <name>
damngood instructions edit <name>
damngood instructions remove <name>
damngood instructions show <name>
damngood instructions sync
```

---

## Skills commands

```bash
damngood skills list
damngood skills add <name>
damngood skills edit <name>
damngood skills remove <name>
damngood skills show <name>
damngood skills sync
```

---

## Client commands

```bash
damngood client list
damngood client register <name> --path <path> [--key mcpServers]
damngood client remove <name>
damngood client enable <name>
damngood client disable <name>
```

---

## Legacy single-client mode

Use `--client` to work against one client directly.

```bash
damngood --client cursor list
damngood --client gemini add myserver --command npx --args -y my-server
```

Supported `--client` values:

- `cursor`
- `gemini`
- `opencode`
- `claude`
- `claude_desktop`
- `generic`
