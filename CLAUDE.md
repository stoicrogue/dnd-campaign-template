# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **Obsidian vault** for managing a tabletop RPG campaign. It contains session notes, character sheets, locations, items, homebrew rules, and campaign recaps.

## Directory Structure

The vault uses numbered prefixes for organization:

- `01 - session-notes/` - Per-session DM prep notes
- `02 - characters/` - NPCs, party members, adversaries, monster stat blocks
  - `main-party/` - Player characters and party reference sheet
  - `adversaries/` - Villain narrative lore pages and stat blocks
  - `allies/` - NPC ally narrative lore pages
  - `monsters/` - Creature stat blocks
- `03 - locations/` - Setting descriptions and maps
- `04 - items/` - Magical and homebrew equipment
- `05 - planning/` - Campaign arcs, encounter design, session prep, DM reference material
- `06 - factions/` - Organizations and power groups
- `07 - rules/` - Homebrew mechanics
- `08 - recap/` - Campaign summaries, quest log, timeline, dramatized narratives

## Automation Scripts

### `_link_characters.py`
Scans markdown files for unlinked character name references and converts them to Obsidian `[[wiki-links]]`. Run from the campaign root directory:
```bash
python _link_characters.py          # apply changes
python _link_characters.py --dry-run  # preview without modifying files
```
- Targets: `01 - session-notes/`, `02 - characters/`, `03 - locations/`, `05 - planning/`, `06 - factions/`, `08 - recap/` (recursive)
- Case-insensitive matching with proper display text (e.g., `elara` → `[[Elara Sunforge|elara]]`)
- Uses pipe syntax for partial names (e.g., `Elara` → `[[Elara Sunforge|Elara]]`)
- Skips: frontmatter, code blocks, headings, text already inside `[[...]]`, self-references
- Safe to re-run — idempotent (0 changes if already linked)
- To add new characters: update the `CHARACTERS` list at the top of the script

### `_link_factions.py`
Same behavior as `_link_characters.py`, but for faction names.
- To add new factions: update the `FACTIONS` list at the top of the script

### `_link_locations.py`
Same behavior as `_link_characters.py`, but for location names.
- To add new locations: update the `LOCATIONS` list at the top of the script

### `obsidian_frontmatter_script.py`
Processes all markdown files to add/update YAML frontmatter. Run from the campaign root directory:
```bash
python obsidian_frontmatter_script.py
```
- Adds standardized frontmatter (tags, date, title, author)
- Derives section tags from parent directory names
- Preserves existing frontmatter values
- Configure `CAMPAIGN_NAME` and `AUTHOR_NAME` at the top of the script

### `add_yaml_frontmatter.py`
Adds frontmatter specifically to session note files matching the pattern `[CAMPAIGN_NAME] Session [NUMBER] (YYYY-MM-DD).md`. Run from `01 - session-notes/`:
```bash
python ../add_yaml_frontmatter.py
```
- Configure `CAMPAIGN_NAME` at the top of the script to match your session file naming

## File Conventions

**Frontmatter format:**
```yaml
---
tags:
  - [section-name]
  - [campaign-name]
date: YYYY-MM-DD
title: [Title]
author:
  - [Author Name]
---
```

**Session note naming:** `[Campaign Name] Session [NUMBER] (YYYY-MM-DD).md`

**Internal linking:** Uses Obsidian wiki-style links `[[Character Name]]`, `[[Location]]`

**Index files:** Each directory has `_index.md` for navigation

## Narrative Lore Page Format

Character and location files follow a consistent narrative structure:

- **Frontmatter:** `tags`, `date`, `title`
- **`# Heading`** followed by **top-level identity bullets** summarizing the entity at a glance
- **`##` thematic sections** organized by narrative significance (not stat-block-first)
- **`[[wiki-links]]`** throughout for cross-referencing characters, locations, and factions
- **Stat blocks** go in separate files (e.g., `Villain Name - Stat Block.md`) linked from the narrative page under a `## Stat Block` section
- **DM reference material** (reveal FAQs, roleplay guides, encounter tables) goes in `05 - planning/`, linked from the narrative page
- **Quotes** from session notes included where available for flavor

## Working with Session Notes

- **Source of truth for campaign state:** Check `08 - recap/` for the most current campaign recap before updating character or faction notes
- **Past tense discipline:** Session prep notes often use future/anticipatory tense. After a session, convert to past tense and record what actually happened vs. what was planned
- **Don't commit** `.obsidian/workspace.json` — it's Obsidian UI state, not campaign content

## Hugo Integration (Optional)

Scripts ensure frontmatter compatibility for publishing campaign notes to a Hugo-based website. A separate project contains the Hugo site and copy scripts.
