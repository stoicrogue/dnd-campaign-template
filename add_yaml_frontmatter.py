#!/usr/bin/env python3
"""
Script to add YAML frontmatter to session note markdown files.
Processes files matching pattern: [CAMPAIGN_NAME] Session [NUMBER] (YYYY-MM-DD).md

Run from inside 01 - session-notes/:
    python ../add_yaml_frontmatter.py
"""

# ===========================================================================
# CONFIG — update these before running
# ===========================================================================
CAMPAIGN_NAME = "[CAMPAIGN_NAME]"   # e.g. "Tempus" — must match your session file names
AUTHOR_NAME   = "[AUTHOR_NAME]"     # e.g. "Mark Molea"
# ===========================================================================

import os
import re
from pathlib import Path


def parse_filename(filename):
    """
    Parse filename to extract session number and date.

    Returns:
        tuple: (session_number, date) or (None, None) if parsing fails
    """
    pattern = rf'{re.escape(CAMPAIGN_NAME)} Session (\d+) \((\d{{4}}-\d{{2}}-\d{{2}})\)\.md'
    match = re.match(pattern, filename)

    if match:
        session_number = match.group(1)
        date = match.group(2)
        return session_number, date

    return None, None


def generate_yaml_frontmatter(session_number, date):
    """Generate YAML frontmatter block."""
    campaign_tag = CAMPAIGN_NAME.lower().replace(' ', '-')
    yaml_block = f"""---
tags:
  - session-notes
  - {campaign_tag}
created: {date}
title: {CAMPAIGN_NAME} Session {session_number}
author:
  - {AUTHOR_NAME}
---

"""
    return yaml_block


def has_yaml_frontmatter(content):
    """Check if content already has YAML frontmatter."""
    return content.strip().startswith('---')


def process_file(file_path):
    """
    Process a single markdown file to add YAML frontmatter.

    Returns:
        bool: True if file was processed, False if skipped
    """
    filename = file_path.name
    session_number, date = parse_filename(filename)

    if not session_number or not date:
        print(f"Skipping {filename}: doesn't match expected pattern")
        return False

    try:
        # Read existing content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if YAML frontmatter already exists
        if has_yaml_frontmatter(content):
            print(f"Skipping {filename}: YAML frontmatter already exists")
            return False

        # Generate YAML frontmatter
        yaml_frontmatter = generate_yaml_frontmatter(session_number, date)

        # Combine frontmatter with existing content
        new_content = yaml_frontmatter + content

        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"Processed {filename}: added YAML frontmatter")
        return True

    except Exception as e:
        print(f"Error processing {filename}: {e}")
        return False


def main():
    """
    Main function to process all matching markdown files in the current directory.
    """
    current_dir = Path('.')
    pattern = f'{CAMPAIGN_NAME} Session *.md'

    # Find all matching files
    markdown_files = list(current_dir.glob(pattern))

    if not markdown_files:
        print(f"No matching markdown files found in current directory.")
        print(f"Looking for pattern: {pattern}")
        return

    print(f"Found {len(markdown_files)} matching files")

    processed_count = 0
    for file_path in sorted(markdown_files):
        if process_file(file_path):
            processed_count += 1

    print(f"\nProcessed {processed_count} out of {len(markdown_files)} files")


if __name__ == "__main__":
    main()
