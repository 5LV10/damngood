# Manage Instructions

Instruction snippets let you define global assistant behavior once.

## Add a snippet

```bash
damngood instructions add coding-style
```

Template:

```markdown
---
description: "Repository coding rules"
clients: [claude, gemini, cursor, windsurf, opencode, continue]
enabled: true
---

Use clear function names.
Prefer readability over cleverness.
Add tests for bug fixes.
```

---

## Edit / show / remove

```bash
damngood instructions show coding-style
damngood instructions edit coding-style
damngood instructions remove coding-style
```

---

## Sync snippets

```bash
damngood instructions sync
```

Output contains per-client snippet counts and target files.

---

## How content is merged

- snippets assigned to a client are combined in order
- snippets are separated by `---`
- combined output is inserted into the managed sentinel block

---

## Example: security baseline snippet

```markdown
---
description: "Security-focused coding defaults"
clients: [claude, gemini, cursor, opencode]
enabled: true
---

Never commit secrets or credentials.
Validate and sanitize all user-controlled input.
Flag shell command injection risks explicitly.
```

---

## Notes for Cursor and Windsurf

- Cursor uses `.mdc` output and includes an always-apply frontmatter block when created.
- Windsurf has a combined character limit; DamnGood warns when near threshold.
