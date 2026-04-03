# Supported Clients

## Capability matrix

| Client | MCP | Instructions | Skills |
|---|---|---|---|
| Claude Code (`claude`) | yes | yes | yes |
| Gemini CLI (`gemini`) | yes | yes | no |
| Cursor (`cursor`) | yes | yes (`.mdc`) | no |
| Windsurf (`windsurf`) | no | yes | no |
| OpenCode (`opencode`) | yes | yes | yes |
| Continue.dev (`continue`) | no | yes | no |
| Claude Desktop (`claude_desktop`) | yes | no | no |

---

## Default paths

### MCP config paths

- `claude`: `~/.claude.json`
- `gemini`: `~/.gemini/settings.json`
- `cursor`: `~/.cursor/mcp.json`
- `opencode`: `~/.config/opencode/opencode.json` (Linux/macOS)
- `claude_desktop`: OS-specific app data path

### Instructions paths

- `claude`: `~/.claude/CLAUDE.md`
- `gemini`: `~/.gemini/GEMINI.md`
- `cursor`: `~/.cursor/rules/damngood-instructions.mdc`
- `windsurf`: `~/.codeium/windsurf/memories/global_rules.md`
- `opencode`: `~/.config/opencode/AGENTS.md`
- `continue`: `~/.continue/rules/damngood.md`

### Skills paths

- `claude`: `~/.claude/skills/<name>/SKILL.md`
- `opencode`: `~/.config/opencode/skills/<name>/SKILL.md`

---

## Custom clients

You can register additional MCP-compatible clients:

```bash
damngood client register mytool --path ~/.mytool/config.json --key mcpServers
```
