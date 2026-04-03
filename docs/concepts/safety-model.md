# Safety Model

DamnGood is designed to avoid destructive edits.

## Instructions safety

Instruction sync uses sentinel markers:

```markdown
<!-- DAMNGOOD:START -->
<!-- Managed by damngood. Run 'damngood instructions sync' to update. -->
...
<!-- DAMNGOOD:END -->
```

Rules:

- only content inside the managed block is replaced
- content outside the block is preserved
- empty managed output removes the block cleanly

---

## Skills safety

Synced `SKILL.md` files begin with:

```markdown
<!-- damngood-managed: do not edit manually -->
```

Rules:

- managed files are safe to update on sync
- non-managed existing files are skipped
- remove operation deletes only managed skill files

---

## Client safety

Each entry has an explicit `clients` list.

Rules:

- no implicit writes to unrelated clients
- disabled clients are excluded from sync
- capabilities are checked before writing

---

## Operational safety checklist

Before large changes:

1. run `damngood client list`
2. verify `clients` assignment in snippet/skill/server
3. run only the sync you need
4. inspect destination files if needed

This keeps rollout controlled and reversible.
