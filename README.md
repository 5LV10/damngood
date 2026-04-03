# DamnGood

A centralized CLI tool to manage **MCP servers**, **agent instructions**, and **skills** across multiple AI coding assistants.

**Documentation:** https://gouthamk16.github.io/damngood/

## The Problem

Managing AI tool configuration across different editors is painful:
- Add the same MCP server to each tool individually
- Copy-paste the same instructions into every tool's config
- Re-create the same slash commands tool by tool
- Keep everything in sync manually across JSON files, Markdown files, and config dirs

## The Solution

DamnGood provides **centralized management** for all three:

1. **MCP Servers** — store in one registry, sync to all tools
2. **Instructions** — write once, push to every tool's global instruction file (CLAUDE.md, GEMINI.md, global_rules.md, etc.)
3. **Skills** — define reusable slash commands centrally, sync as native SKILL.md files

## Supported Clients

Auto-discovered clients:

| Client | MCP | Instructions | Skills |
|--------|-----|-------------|--------|
| **Claude Code** | ✓ `~/.claude.json` | ✓ `~/.claude/CLAUDE.md` | ✓ `~/.claude/skills/` |
| **Gemini CLI** | ✓ `~/.gemini/settings.json` | ✓ `~/.gemini/GEMINI.md` | — |
| **Cursor** | ✓ `~/.cursor/mcp.json` | ✓ `~/.cursor/rules/damngood-instructions.mdc` | — |
| **Windsurf** | — | ✓ `~/.codeium/windsurf/memories/global_rules.md` | — |
| **OpenCode** | ✓ `~/.config/opencode/opencode.json` | ✓ `~/.config/opencode/AGENTS.md` | ✓ `~/.config/opencode/skills/` |
| **Continue.dev** | — | ✓ `~/.continue/rules/damngood.md` | — |
| **Claude Desktop** | ✓ platform app data | — | — |

Plus register any custom MCP-compatible tool.

## Install

```bash
git clone https://github.com/5LV10/damngood.git
cd damngood
pip install -e .

damngood --help
```

## Quick Start

```bash
# See which AI tools are installed
damngood client list

# --- MCP Servers ---
damngood import              # pull existing MCP configs into the registry
damngood add filesystem      # add a new server (opens $EDITOR)
damngood sync                # push to all assigned clients

# --- Agent Instructions ---
damngood instructions add coding-style   # write a snippet (opens $EDITOR)
damngood instructions sync               # push to CLAUDE.md, GEMINI.md, etc.

# --- Skills ---
damngood skills add review-pr            # create a skill (opens $EDITOR)
damngood skills sync                     # deploy to ~/.claude/skills/ etc.
```

---

## MCP Servers

### How it works

Servers are stored in `~/.damngood/registry.json`. The `clients` array controls which tools receive each server on sync.

```json
{
  "servers": {
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem"],
      "env": {},
      "clients": ["cursor", "gemini"]
    }
  }
}
```

### Commands

```bash
damngood list                  # list servers in central registry
damngood add <name>            # add via JSON editor
damngood edit <name>           # edit via JSON editor
damngood remove <name>         # remove from registry
damngood show <name>           # show details
damngood sync                  # push to all assigned clients
damngood import                # import from existing client configs
```

### Example

```bash
$ damngood add github
# Editor opens with template — fill in command, args, env, clients
Added server 'github' to central registry

$ damngood sync
  ✓ cursor    →  2 server(s)  (~/.cursor/mcp.json)
  ✓ gemini    →  1 server(s)  (~/.gemini/settings.json)
```

---

## Agent Instructions

Write markdown instruction snippets once and push them to every tool's global instruction file. Each tool reads these files automatically on startup.

### How it works

Snippets are stored in `~/.damngood/instructions/`. On sync, damngood inserts a **managed section** into each tool's instruction file using HTML comment sentinels:

```markdown
# My personal notes (not touched by damngood)

<!-- DAMNGOOD:START -->
<!-- Managed by damngood. Run 'damngood instructions sync' to update. -->

Always prefer TypeScript over JavaScript.
Use conventional commits for all commit messages.

<!-- DAMNGOOD:END -->

More personal notes (also untouched)
```

- User content above/below the sentinels is **never modified**
- Running sync twice is **idempotent**
- Removing all snippets from a client **removes the sentinels entirely**

### Adding a snippet

```bash
$ damngood instructions add coding-style
```

Your editor opens with a template:

```markdown
---
description: "Brief description of this instruction snippet"
clients: [claude, gemini, cursor, windsurf, opencode, continue]
enabled: true
---

Write your instruction content here in plain Markdown.
```

Edit the frontmatter to set which clients receive this snippet, write your instructions in the body, save and close.

### Commands

```bash
damngood instructions list              # list all snippets
damngood instructions add <name>        # add snippet (opens editor)
damngood instructions edit <name>       # edit snippet
damngood instructions remove <name>     # remove from registry
damngood instructions show <name>       # show content and metadata
damngood instructions sync              # push to all assigned clients
```

### Client targets

| Client | Instructions file |
|--------|------------------|
| `claude` | `~/.claude/CLAUDE.md` |
| `gemini` | `~/.gemini/GEMINI.md` |
| `cursor` | `~/.cursor/rules/damngood-instructions.mdc` (always-apply rule) |
| `windsurf` | `~/.codeium/windsurf/memories/global_rules.md` |
| `opencode` | `~/.config/opencode/AGENTS.md` |
| `continue` | `~/.continue/rules/damngood.md` |

> **Windsurf note**: Windsurf has a combined 12,000 character limit. DamnGood warns if you approach it.

---

## Skills

Define reusable slash commands centrally and sync them as native `SKILL.md` files to Claude Code and OpenCode.

### How it works

Skills are stored in `~/.damngood/skills/<name>/content.md`. On sync, damngood writes a native `SKILL.md` to each client's skills directory. Files written by damngood are marked with a managed header so they're never accidentally overwritten.

### Adding a skill

```bash
$ damngood skills add review-pr
```

Your editor opens with a template:

```markdown
---
description: "What this skill does"
user-invocable: true
allowed-tools: [Read, Grep, Bash]
clients: [claude, opencode]
enabled: true
---

# review-pr

Review a pull request for correctness, style, and potential issues.

## Steps

1. Read the diff with `git diff`
2. Check for security issues
3. Summarize findings
```

### Commands

```bash
damngood skills list              # list all skills
damngood skills add <name>        # add skill (opens editor)
damngood skills edit <name>       # edit skill
damngood skills remove <name>     # remove from registry + delete SKILL.md files
damngood skills show <name>       # show content and metadata
damngood skills sync              # deploy to all assigned clients
```

### Client targets

| Client | Skills directory |
|--------|-----------------|
| `claude` | `~/.claude/skills/<name>/SKILL.md` |
| `opencode` | `~/.config/opencode/skills/<name>/SKILL.md` |

---

## Client Management

```bash
damngood client list                    # show all discovered clients and their status
damngood client enable <name>           # include client in all syncs
damngood client disable <name>          # exclude client from syncs
damngood client register <name> --path <path>   # add a custom MCP tool
damngood client remove <name>           # remove a custom registration
```

---

## Configuration Files

All configuration lives in `~/.damngood/`:

```
~/.damngood/
  registry.json              MCP server registry
  clients.json               Registered AI tool clients
  instructions/
    index.json               Snippet metadata and client assignments
    <name>.md                Snippet content (one file per snippet)
  skills/
    index.json               Skill metadata and client assignments
    <name>/
      content.md             Skill body
```

---

## Commands Reference

### MCP Servers

| Command | Description |
|---------|-------------|
| `list` | List centrally managed servers |
| `add <name>` | Add server via JSON editor |
| `edit <name>` | Edit server via JSON editor |
| `remove <name>` | Remove from central registry |
| `show <name>` | Show server details |
| `sync` | Sync MCP servers to all assigned clients |
| `import` | Import existing client configs |

### Instructions

| Command | Description |
|---------|-------------|
| `instructions list` | List all snippets |
| `instructions add <name>` | Add snippet via editor |
| `instructions edit <name>` | Edit snippet |
| `instructions remove <name>` | Remove snippet |
| `instructions show <name>` | Show snippet details |
| `instructions sync` | Push snippets to all assigned clients |

### Skills

| Command | Description |
|---------|-------------|
| `skills list` | List all skills |
| `skills add <name>` | Add skill via editor |
| `skills edit <name>` | Edit skill |
| `skills remove <name>` | Remove skill + delete SKILL.md files |
| `skills show <name>` | Show skill details |
| `skills sync` | Deploy skills to all assigned clients |

### Client Management

| Command | Description |
|---------|-------------|
| `client list` | List registered clients |
| `client register <name>` | Register new client |
| `client remove <name>` | Remove registered client |
| `client enable <name>` | Enable client for sync |
| `client disable <name>` | Disable client |

### Single-Client Mode (`--client`)

| Command | Description |
|---------|-------------|
| `--client cursor list` | List Cursor's MCP servers |
| `--client cursor add <name>` | Add to Cursor only |
| `--client cursor remove <name>` | Remove from Cursor only |

---

## Tips

- **Auto-discovery**: Run `damngood client list` after installing a new AI tool — it will be detected automatically
- **Selective sync**: Use the `clients` array to control exactly which tools get each server/snippet/skill
- **Non-destructive instructions**: DamnGood only manages the content between its sentinel markers — your personal notes in CLAUDE.md etc. are never touched
- **Quick edits**: `damngood instructions edit <name>` re-opens the editor with your existing content pre-loaded
- **Migration**: Use `damngood import` to move existing MCP configs into the central registry

## Why Use This?

- **One source of truth** — central registry eliminates config drift across tools
- **Write once** — instructions and skills deploy everywhere with a single command
- **Safe** — managed sections never overwrite user content; skill files check for the managed marker before overwriting
- **No new dependencies** — pure Python stdlib plus `rich` for the terminal UI
- **Cross-platform** — Linux, macOS, and Windows paths handled automatically
