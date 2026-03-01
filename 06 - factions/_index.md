---
tags:
  - factions
date: YYYY-MM-DD
title: Factions
---

# Factions

Organizations, power groups, and institutions that shape the world. One file per faction.

## Faction Page Format

```markdown
# [Faction Name]

- **Type:** Political / Religious / Criminal / Military / Scholarly
- **Alignment:** [General moral alignment]
- **Base of Operations:** [[Location]]
- **Leader:** [[Character Name]]
- **Status:** Active / Weakened / Destroyed

## Overview

*What is this faction? What do they want?*

## History

*How did they form? Key events.*

## Structure

*How are they organized? Ranks, cells, chapters.*

## Methods

*How do they pursue their goals?*

## Relationship to the Party

*Have they clashed? Are they allied? Neutral? Does the party even know they exist?*

## Notable Members

- [[Character Name]] — role
- [[Character Name]] — role

## DM Notes

*Secrets, future plans, internal conflicts.*
```

## Adding Factions to Wiki-Link Automation

After creating a new faction page, add it to `_link_factions.py` in the campaign root:

```python
FACTIONS = [
    ("Full Faction Name",  "Full Faction Name",  None),
]
```

Then run:
```bash
python _link_factions.py
```
