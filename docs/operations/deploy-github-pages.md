# Deploy with GitHub Pages

This docs site is static and can be hosted directly from GitHub.

## Option A: automatic deploy via GitHub Actions (recommended)

1. Push repository changes.
2. Ensure workflow file exists: `.github/workflows/docs.yml`.
3. In GitHub, open `Settings -> Pages`.
4. Set source to `GitHub Actions`.

Every push to `main` builds and deploys docs.

---

## Option B: branch-based deploy

1. Run local build:

```bash
mkdocs build
```

2. Publish generated site manually to pages branch.

Option B is slower and easier to break; prefer Option A.

---

## Local preview

```bash
pip install -e '.[docs]'
mkdocs serve
```

Open `http://127.0.0.1:8000`.
