# Manage Skills

Skills are reusable prompts/workflows synced as native `SKILL.md` files.

## Add a skill

```bash
damngood skills add review-pr
```

Template:

```markdown
---
description: "Review pull requests for correctness and risk"
user-invocable: true
allowed-tools: [Read, Grep, Bash]
clients: [claude, opencode]
enabled: true
---

# review-pr

Review PR changes and report:
1. correctness bugs
2. security concerns
3. missing tests
4. rollback or migration risks
```

---

## Edit / show / remove

```bash
damngood skills show review-pr
damngood skills edit review-pr
damngood skills remove review-pr
```

---

## Sync skills

```bash
damngood skills sync
```

DamnGood writes one `SKILL.md` per assigned client and skill.

---

## File ownership and safety

- files created by DamnGood include a managed marker
- existing files without managed marker are never overwritten
- remove command deletes managed files for assigned clients

---

## Example skill library structure

```text
~/.damngood/skills/
  index.json
  review-pr/
    content.md
  debug-test-failures/
    content.md
```

Use one focused skill per repeated task.
