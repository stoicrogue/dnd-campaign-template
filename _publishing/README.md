# Publishing to Hugo

This directory contains everything needed to publish your campaign notes as a static website using [Hugo](https://gohugo.io/) and the [Terminal theme](https://github.com/panr/hugo-theme-terminal).

The pipeline converts your Obsidian vault (with `[[wiki-links]]` and `![[image]]` embeds) into a Hugo-compatible content directory, then deploys to any static host via GitHub Actions.

---

## How It Works

```
Obsidian Vault  →  convert_wikilinks.py  →  Hugo content/
                →  sync-obsidian-images.py  →  Hugo static/images/
                                           ↓
                                     hugo --minify
                                           ↓
                                  GitHub Actions deploy
```

`update.sh` runs both Python scripts in sequence. After running it, commit the Hugo site repo and push to `main` — GitHub Actions handles the build and deploy.

---

## One-Time Setup

### 1. Create the Hugo site repo

Create a new git repo for your Hugo site (separate from the vault):

```bash
mkdir my-campaign-site
cd my-campaign-site
git init
```

Copy everything from `_publishing/hugo-site/` into it.

### 2. Add the Terminal theme as a submodule

```bash
git submodule add https://github.com/panr/hugo-theme-terminal.git themes/terminal
```

### 3. Configure the Hugo site

Edit `hugo.toml` and replace the placeholders:
- `[CAMPAIGN_NAME]` — your campaign name (e.g., "Tempus")
- `[AUTHOR_NAME]` — your name
- `[AUTHOR_URL]` — your website or GitHub profile URL
- `[SITE_URL]` — the published site URL

### 4. Configure the publishing scripts

In this `_publishing/` directory, update the config block at the top of each script:

**`update.sh`**
```bash
VAULT_PATH="/path/to/your/vault"
CONTENT_PATH="/path/to/hugo-site/content"
PROJECT_PATH="/path/to/hugo-site"
```

**`sync-obsidian-images.py`**
```python
CONTENT_DIR     = "/path/to/hugo-site/content/"
ATTACHMENTS_DIR = "/path/to/obsidian/attachments/"
STATIC_IMAGES_DIR = "/path/to/hugo-site/static/images/"
```

### 5. Set up GitHub Actions deployment

In the Hugo site repo, add these secrets under Settings → Secrets → Actions:

| Secret | Value |
|--------|-------|
| `DREAMHOST_SSH_KEY` | Your Ed25519 private key (for DreamHost) |
| `DREAMHOST_HOST` | SSH hostname |
| `DREAMHOST_USER` | SSH username |
| `DREAMHOST_PATH` | Remote path to deploy to |

If you're deploying to a different host (Netlify, Vercel, GitHub Pages, etc.), edit `.github/workflows/deploy.yml` to match your host's deploy method.

---

## Daily Workflow

1. Write and edit notes in Obsidian as normal (use `[[wiki-links]]`, `![[images]]`)
2. Run `./update.sh` from inside the `_publishing/` directory
3. Review the result with `hugo serve` in the Hugo site directory
4. `git add . && git commit && git push` in the Hugo site repo
5. GitHub Actions builds and deploys automatically

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `update.sh` | Orchestrator — runs both Python scripts in sequence |
| `convert_wikilinks.py` | Converts `[[wiki-links]]` to Hugo markdown URLs; slugifies directory names |
| `sync-obsidian-images.py` | Converts `![[image.png]]` embeds to standard markdown; copies images to `static/images/` |

---

## Hugo Site Contents (`hugo-site/`)

| Path | Purpose |
|------|---------|
| `hugo.toml` | Hugo site configuration (title, menus, theme settings) |
| `layouts/index.html` | Homepage layout — renders `_index.md` content |
| `layouts/_default/section.html` | Section pages — renders `_index.md` + hierarchical page list |
| `layouts/_default/_markup/render-blockquote.html` | Obsidian callout support (`> [!note]`, `> [!warning]`, etc.) |
| `layouts/partials/footer.html` | Custom footer with attribution and CC license |
| `archetypes/default.md` | Default Hugo archetype |
| `.github/workflows/deploy.yml` | CI/CD: build with Hugo, deploy via rsync over SSH |
| `content/` | Populated by `update.sh` — do not edit manually |
| `static/images/` | Populated by `sync-obsidian-images.py` — do not edit manually |
