---
tags:
  - recap
date: YYYY-MM-DD
title: Recap
---

# Recap

Campaign summaries, timelines, quest logs, and dramatized narratives. This folder serves as the long-running historical record of the campaign.

## Suggested Files

| File | Purpose |
|------|---------|
| `[Campaign Name] Campaign Recap.md` | Rolling campaign summary — update after each session |
| `Quest Log.md` | Active and completed quests with outcomes |
| `Timeline.md` | In-world chronology of major events |
| `[Campaign Name] Campaign Dramatization.md` | Prose narrative retelling of the story |

## Campaign Recap Format

The `Campaign Recap.md` is the **source of truth** for campaign state. Update it after each session.

```markdown
# [Campaign Name] Campaign Recap

## Current Status (as of Session [N])

*Brief summary of where things stand right now.*

## Session Summaries

### Session [N] — [Date]

*What happened, in 2-5 sentences.*

### Session [N-1] — [Date]

*What happened.*
```

## Dramatization Note

The dramatization file (`[Campaign Name] Campaign Dramatization.md`) is **excluded from wiki-link automation** (see `SKIP_FILES` in the link scripts). This prevents over-linking in prose narrative text.

## Quest Log Format

```markdown
# Quest Log

## Active Quests

### [Quest Name]
- **Given by:** [[NPC Name]]
- **Objective:** ...
- **Current status:** ...

## Completed Quests

### [Quest Name]
- **Completed:** Session [N]
- **Outcome:** ...
```
