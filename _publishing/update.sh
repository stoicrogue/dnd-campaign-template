#!/usr/bin/env bash
set -euo pipefail

# ===========================================================================
# CONFIG — update these paths before running
# ===========================================================================
VAULT_PATH="/path/to/your/obsidian/vault"      # e.g. /c/Users/you/obsidian/my-campaign
CONTENT_PATH="/path/to/your/hugo-site/content" # e.g. /c/Projects/my-campaign-site/content
PROJECT_PATH="/path/to/your/hugo-site"         # e.g. /c/Projects/my-campaign-site
# ===========================================================================

cd "$(dirname "$0")"  # run from _publishing/ directory

echo "=== Converting Obsidian notes to Hugo markdown ==="
python -u convert_wikilinks.py \
  --vault "$VAULT_PATH" \
  --content "$CONTENT_PATH" \
  --clean

echo "=== Copying and fixing image links ==="
python sync-obsidian-images.py

echo "✅ Sync complete! Run 'hugo serve' in $PROJECT_PATH to preview."
