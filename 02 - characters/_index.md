---
tags:
  - characters
date: YYYY-MM-DD
title: Characters
---

# Characters

All campaign characters organized into four subdirectories.

## Subdirectories

| Folder | Contents |
|--------|---------|
| `main-party/` | Player characters and party reference sheets |
| `allies/` | Friendly NPCs with narrative lore pages |
| `adversaries/` | Villains with narrative lore pages and linked stat blocks |
| `monsters/` | Creature stat blocks (standard, homebrew, MCDM minions) |

## Narrative Lore Page Format

Character pages in `allies/` and `adversaries/` follow this structure:

1. **Frontmatter** — tags, date, title
2. **`# Name`** — followed by top-level identity bullets (role, affiliation, location, status)
3. **`##` thematic sections** — origins, goals, personality, relationship to the party
4. **`## Stat Block`** — link(s) to separate stat block file(s)

Keep narrative pages **readable prose** — save mechanical details (HP, AC, abilities) for the separate stat block files.

## Adding Characters to Wiki-Link Automation

After creating a new character page, add the character to `_link_characters.py` in the campaign root:

```python
CHARACTERS = [
    ("Full Character Name",  "Full Character Name",  None),
    ("Short Name",           "Full Character Name",  "Short Name"),  # if they have a common short name
]
```

Then run:
```bash
python _link_characters.py
```
