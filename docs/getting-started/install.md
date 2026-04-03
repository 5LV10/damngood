# Install

## Requirements

- Python `3.7+`
- Git
- a terminal shell

Check your Python version:

```bash
python3 --version
```

---

## Clone and install

```bash
git clone https://github.com/5LV10/damngood.git
cd damngood
pip install -e .
```

Verify the CLI is available:

```bash
damngood --help
```

If `damngood` is not found, run through Python directly:

```bash
python3 damngood-cli.py --help
```

---

## Optional: local virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

---

## Optional: docs dependencies

If you want to run this docs site locally:

```bash
pip install -e '.[docs]'
mkdocs serve
```

Open `http://127.0.0.1:8000`.
