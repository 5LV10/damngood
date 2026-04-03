# Troubleshooting

## `damngood: command not found`

Use Python entrypoint directly:

```bash
python3 damngood-cli.py --help
```

If that works, reinstall editable package:

```bash
pip install -e .
```

---

## No clients detected

Run:

```bash
damngood client list
```

If empty:

- launch your target tool once so config directories are created
- verify expected config locations exist
- register custom client if needed

---

## Editor did not open for `add` or `edit`

Set editor explicitly:

```bash
export EDITOR=nano
```

Then retry command.

---

## Snippet or skill did not sync

Check all three:

1. item is `enabled: true`
2. client is included in item `clients`
3. client is enabled in `damngood client list`

Then run sync again.

---

## Skill file was skipped

If target `SKILL.md` exists and lacks the managed marker, DamnGood skips it by design.

Options:

- move/rename manual file
- remove manual file
- rerun `damngood skills sync`

---

## Windsurf size warning

Windsurf has a combined instruction character limit.

If warned:

- reduce snippet length
- disable lower-priority snippets for `windsurf`
- split snippets and target only necessary clients
