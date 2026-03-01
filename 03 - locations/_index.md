---
tags:
  - locations
date: YYYY-MM-DD
title: Locations
---

# Locations

World locations, settlements, dungeons, and points of interest. Each significant location gets its own file.

## Narrative Location Page Format

```markdown
# [Location Name]

- **Type:** City / Dungeon / Wilderness / Planar Location
- **Region:** [Broader geographic context]
- **Factions:** [[Faction Name]]
- **Status:** Active / Abandoned / Destroyed

## Description

*What does it look, sound, smell like? First impressions.*

## History

*How did this place come to be? What happened here?*

## Notable Features

*Specific rooms, districts, landmarks worth calling out.*

## NPCs Here

*Who lives or works here? Link to character pages.*

## Encounter Notes

*Combat or social encounters set in this location.*

## DM Notes

*Secrets, hooks, things the players don't know yet.*
```

## Adding Locations to Wiki-Link Automation

After creating a new location page, add it to `_link_locations.py` in the campaign root:

```python
LOCATIONS = [
    ("Full Location Name",  "Full Location Name",  None),
    ("Short Name",          "Full Location Name",  "Short Name"),  # optional
]
```

Then run:
```bash
python _link_locations.py
```
