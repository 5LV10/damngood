# Team Onboarding Playbook

Use this when rolling out DamnGood to a team.

## Goal

Get every developer to the same assistant baseline in under 30 minutes.

## Step 1: define baseline assets

Create:

- 3-5 core instruction snippets (style, testing, security)
- 2-3 reusable skills (PR review, failure triage)
- common MCP servers used by the team

---

## Step 2: distribute bootstrap commands

```bash
git clone https://github.com/5LV10/damngood.git
cd damngood
pip install -e .
damngood client list
damngood import
```

---

## Step 3: apply central standards

```bash
damngood instructions sync
damngood skills sync
damngood sync
```

Order is flexible; this sequence is easiest to communicate.

---

## Step 4: verify outcomes

Ask each dev to run:

```bash
damngood list
damngood instructions list
damngood skills list
```

And confirm target client files are updated.

---

## Step 5: maintain and iterate

- update snippets/skills centrally
- sync after changes
- keep a changelog entry in your main project repo

---

## Suggested baseline snippets

1. `coding-style`
2. `test-discipline`
3. `security-defaults`
4. `pr-guidelines`

Use concise instructions and avoid overlapping rules.
