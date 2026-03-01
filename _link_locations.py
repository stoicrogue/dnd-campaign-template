"""
Link Locations in Campaign Notes
==================================
Scans markdown files and converts unlinked location name references
into Obsidian wiki-links ([[...]]).

Usage:
    python _link_locations.py          # apply changes
    python _link_locations.py --dry-run  # preview changes without writing
"""

import os
import re
import sys

# ===========================================================================
# CONFIG — update these before running
# ===========================================================================
CAMPAIGN_NAME = "[CAMPAIGN_NAME]"   # e.g. "Tempus"
# ---------------------------------------------------------------------------
# Location definitions: (search_term, link_target, display_text_or_None)
#
# Order matters — longer / more specific names MUST come first to avoid
# partial-match collisions.
#
# Format:
#   ("Location Name",  "Location Name",  None),
#
# For locations with common short names:
#   ("Ironspire Citadel",  "Ironspire Citadel",  None),
#   ("Ironspire",          "Ironspire Citadel",  "Ironspire"),
# ---------------------------------------------------------------------------
LOCATIONS = [
    # Add your locations here:
    # ("Location Name",  "Location Name",  None),
]
# ===========================================================================

BASE_DIR = os.path.dirname(__file__)
TARGET_DIRS = [
    os.path.join(BASE_DIR, "01 - session-notes"),
    os.path.join(BASE_DIR, "02 - characters"),
    os.path.join(BASE_DIR, "03 - locations"),
    os.path.join(BASE_DIR, "05 - planning"),
    os.path.join(BASE_DIR, "06 - factions"),
    os.path.join(BASE_DIR, "08 - recap"),
]

SKIP_FILES = [
    f"{CAMPAIGN_NAME} Campaign Dramatization.md",
]


def build_replacement(target, display):
    """Return the wiki-link string."""
    if display is None:
        return f"[[{target}]]"
    return f"[[{target}|{display}]]"


def is_inside_link(text, start, end):
    """Check if position start..end is already inside [[ ... ]]."""
    search_start = max(0, start - 200)
    before = text[search_start:start]
    after = text[end:end + 200]

    last_open = before.rfind("[[")
    last_close = before.rfind("]]")

    if last_open != -1 and (last_close == -1 or last_open > last_close):
        next_close = after.find("]]")
        if next_close != -1:
            return True
    return False


def process_line(line, in_frontmatter, in_code_block, locations=None):
    """Process a single line, returning (modified_line, in_frontmatter, in_code_block)."""

    stripped = line.strip()
    if stripped == "---":
        if in_frontmatter is None:
            return line, True, in_code_block
        elif in_frontmatter:
            return line, False, in_code_block
        return line, in_frontmatter, in_code_block

    if in_frontmatter:
        return line, in_frontmatter, in_code_block

    if stripped.startswith("```"):
        return line, in_frontmatter, not in_code_block

    if in_code_block:
        return line, in_frontmatter, in_code_block

    if stripped.startswith("#"):
        return line, in_frontmatter, in_code_block

    for search_term, target, display in (locations if locations is not None else LOCATIONS):
        pattern = re.compile(r'(?<!\[)\b(' + re.escape(search_term) + r')\b(?!\])', re.IGNORECASE)

        new_line = ""
        last_end = 0
        for match in pattern.finditer(line):
            ms, me = match.start(), match.end()
            if is_inside_link(line, ms, me):
                continue
            matched_text = match.group(1)
            if matched_text != search_term:
                rep = f"[[{target}|{matched_text}]]"
            else:
                rep = build_replacement(target, display)
            new_line += line[last_end:ms] + rep
            last_end = me

        if last_end > 0:
            new_line += line[last_end:]
            line = new_line

    return line, in_frontmatter, in_code_block


def process_file(filepath, dry_run=False):
    """Process a single markdown file. Returns (filepath, num_changes) or None."""
    with open(filepath, "r", encoding="utf-8") as f:
        original = f.read()

    # Skip locations whose link target matches this file (no self-links)
    file_stem = os.path.splitext(os.path.basename(filepath))[0]
    locations = [(s, t, d) for s, t, d in LOCATIONS if t != file_stem]

    lines = original.split("\n")
    new_lines = []
    in_frontmatter = None
    in_code_block = False

    for line in lines:
        new_line, in_frontmatter, in_code_block = process_line(line, in_frontmatter, in_code_block, locations)
        new_lines.append(new_line)

    result = "\n".join(new_lines)

    if result != original:
        old_links = original.count("[[")
        new_links = result.count("[[")
        num_new = new_links - old_links

        if not dry_run:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(result)

        return (filepath, num_new)

    return None


def main():
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("=== DRY RUN — no files will be modified ===\n")

    md_files = []
    for target_dir in TARGET_DIRS:
        if not os.path.isdir(target_dir):
            print(f"Warning: Directory not found: {target_dir}")
            continue
        for root, dirs, files in os.walk(target_dir):
            for f in sorted(files):
                if f.endswith(".md") and f != "_index.md" and f not in SKIP_FILES:
                    md_files.append(os.path.join(root, f))

    md_files.sort()
    print(f"Scanning {len(md_files)} markdown files...\n")

    total_changes = 0
    files_changed = 0
    current_dir = None

    for filepath in md_files:
        parent = os.path.dirname(filepath)
        rel_parent = os.path.relpath(parent, BASE_DIR)
        if rel_parent != current_dir:
            current_dir = rel_parent
            print(f"[{current_dir}]")

        result = process_file(filepath, dry_run=dry_run)
        if result:
            fname = os.path.basename(result[0])
            count = result[1]
            print(f"  {fname}: +{count} links")
            total_changes += count
            files_changed += 1

    print(f"\n{'Would add' if dry_run else 'Added'} {total_changes} links across {files_changed} files.")

    if dry_run:
        print("\nRun without --dry-run to apply changes.")


if __name__ == "__main__":
    main()
