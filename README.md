# D&D Campaign Notebook Template

A structured Obsidian vault template for running tabletop RPG campaigns. Includes a consistent folder hierarchy, automation scripts for maintaining wiki-links and frontmatter, and a session prep template based on the [Lazy Dungeon Master](https://slyflourish.com/returnofthelazydm.html) method.

Built from the [Tempus campaign](https://tempus.zennotes.net/) (45+ sessions, November 2022 - February 2026).

---

## Quick Start

1. **Clone or copy** this repo into your Obsidian vaults folder:
   ```bash
   git clone https://github.com/stoicrogue/dnd-campaign-template my-campaign
   ```
   Or just download the ZIP and rename the folder.

2. **Open in Obsidian:** File → Open Vault → select your campaign folder.

3. **Configure the scripts:** Open each Python script and update the config block at the top:
   - `CAMPAIGN_NAME` — your campaign's name (used in frontmatter tags and file patterns)
   - `AUTHOR_NAME` — your name (used in frontmatter)
   - Entity lists (`CHARACTERS`, `FACTIONS`, `LOCATIONS`) — add entries as your campaign grows

4. **Start writing:** Session notes go in `01 - session-notes/`. Copy the template from `05 - planning/Session Notes Template.md`.

---

## Directory Tour

| Folder | Purpose |
|--------|---------|
| `01 - session-notes/` | Per-session DM prep notes |
| `02 - characters/` | All characters: party, allies, adversaries, monsters |
| `03 - locations/` | World locations and setting descriptions |
| `04 - items/` | Magic items and homebrew equipment |
| `05 - planning/` | Campaign arcs, encounter design, DM reference material |
| `06 - factions/` | Organizations and power groups |
| `07 - rules/` | Homebrew mechanics |
| `08 - recap/` | Session summaries, timelines, dramatized narratives |

See each folder's `_index.md` for detailed guidance.

---

## Script Reference

All scripts run from the campaign root folder (where this README lives).

### `_link_characters.py`
Scans markdown files and converts unlinked character name mentions into Obsidian `[[wiki-links]]`.

```bash
python _link_characters.py           # apply changes
python _link_characters.py --dry-run # preview without modifying files
```

Add characters to the `CHARACTERS` list at the top of the script. Order matters — put longer/more specific names before shorter ones (e.g., "Elara Sunforge" before "Elara").

### `_link_factions.py`
Same as above, for faction names.

```bash
python _link_factions.py
python _link_factions.py --dry-run
```

### `_link_locations.py`
Same as above, for location names.

```bash
python _link_locations.py
python _link_locations.py --dry-run
```

### `obsidian_frontmatter_script.py`
Adds or updates YAML frontmatter on all markdown files (tags, date, title, author).

```bash
python obsidian_frontmatter_script.py
```

### `add_yaml_frontmatter.py`
Adds frontmatter to session note files matching the naming pattern `[CAMPAIGN_NAME] Session [NUMBER] (YYYY-MM-DD).md`. Run from inside `01 - session-notes/`.

```bash
cd "01 - session-notes"
python ../add_yaml_frontmatter.py
```

---

## File Naming Conventions

**Session notes:** `[Campaign Name] Session [NUMBER] (YYYY-MM-DD).md`
- Example: `Tempus Session 23 (2024-03-15).md`

**Character files:** Use the character's full name as the filename.
- Narrative lore page: `Elara Sunforge.md`
- Stat block (separate file): `Elara Sunforge - Stat Block.md`

**Stat blocks** go in separate files linked from the narrative page, keeping lore pages readable.

---

## Frontmatter Format

```yaml
---
tags:
  - [section-name]
  - [campaign-name]
date: YYYY-MM-DD
title: [Title]
author:
  - Your Name
---
```

The `obsidian_frontmatter_script.py` handles this automatically using the config block at the top of the script.

---

## Narrative Lore Page Format

Character and location pages follow a consistent structure:

1. **Frontmatter** — tags, date, title
2. **`# Heading`** — followed by top-level identity bullets summarizing the entity at a glance
3. **`##` thematic sections** — organized by narrative significance (not stat-block-first)
4. **`[[wiki-links]]`** throughout — cross-references to characters, locations, factions
5. **`## Stat Block`** section at the end — links to separate stat block files

Example structure:
```markdown
---
tags:
  - Villain
  - my-campaign
date: 2024-01-01
title: Malachar the Dread
---

# Malachar the Dread

- **Role:** Primary antagonist, Season 2
- **Affiliation:** [[The Ashen Court]]
- **Location:** [[Ironspire Citadel]]
- **Status:** At large

## Origins

## Goals

## Personality

## Relationship to the Party

## Stat Block

See [[Malachar - Stat Block]] for combat statistics.
```

---

## Session Prep Template

A blank Lazy Dungeon Master session prep template is in `05 - planning/Session Notes Template.md`. Copy it to `01 - session-notes/` and rename it for each session.

The template includes: Strong Start, Scenes, Secrets & Clues, Fantastic Locations, NPCs, Monsters, Treasure, and a Cold Open section.

---

## Hugo Publishing (Optional)

The `_publishing/` directory contains a complete publishing pipeline for turning your campaign notes into a static website using [Hugo](https://gohugo.io/).

It includes:
- `convert_wikilinks.py` — converts `[[wiki-links]]` to Hugo markdown URLs
- `sync-obsidian-images.py` — copies images from Obsidian to the Hugo `static/` directory
- `update.sh` — orchestrator; run this to sync the vault to Hugo
- `hugo-site/` — ready-to-use Hugo site scaffold with the Terminal theme, custom layouts, and a GitHub Actions deploy workflow

See `_publishing/README.md` for full setup instructions.
