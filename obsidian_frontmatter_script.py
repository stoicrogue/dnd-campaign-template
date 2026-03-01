#!/usr/bin/env python3
"""
Script to add frontmatter to Obsidian markdown files in the campaign folder.
Run this script from within the campaign root directory.
"""

# ===========================================================================
# CONFIG — update these before running
# ===========================================================================
CAMPAIGN_NAME = "[CAMPAIGN_NAME]"   # e.g. "tempus" (used as a frontmatter tag)
AUTHOR_NAME   = "[AUTHOR_NAME]"     # e.g. "Mark Molea"
# ===========================================================================

import os
import stat
from pathlib import Path
from datetime import datetime
import platform


def get_creation_date(file_path):
    """Get file creation date in yyyy-mm-dd format."""
    try:
        if platform.system() == 'Windows':
            # On Windows, st_ctime is creation time
            creation_time = os.path.getctime(file_path)
        else:
            # On Unix/Linux/Mac, try to get birth time, fall back to ctime
            stat_result = os.stat(file_path)
            try:
                # macOS has st_birthtime
                creation_time = stat_result.st_birthtime
            except AttributeError:
                # Linux doesn't have creation time, use ctime (last metadata change)
                creation_time = stat_result.st_ctime

        return datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d')
    except Exception as e:
        print(f"Warning: Could not get creation date for {file_path}: {e}")
        # Fallback to current date
        return datetime.now().strftime('%Y-%m-%d')


def parse_frontmatter(content):
    """Parse YAML frontmatter from file content. Returns (frontmatter_dict, body_content)."""
    lines = content.split('\n')

    if not lines or lines[0].strip() != '---':
        return None, content

    # Find the closing ---
    frontmatter_lines = []
    body_start = 0

    for i, line in enumerate(lines[1:], 1):
        if line.strip() == '---':
            body_start = i + 1
            break
        frontmatter_lines.append(line)
    else:
        # No closing ---, treat as no frontmatter
        return None, content

    # Parse the frontmatter into a simple dict
    frontmatter_dict = {}
    current_key = None

    for line in frontmatter_lines:
        line = line.rstrip()
        if ':' in line and not line.startswith('  '):
            # New key-value pair
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            if value.startswith('[') or not value:
                # List or empty value
                if value.startswith('['):
                    # Simple list on one line: key: [item1, item2]
                    frontmatter_dict[key] = value
                else:
                    # Multi-line list starting
                    frontmatter_dict[key] = []
                    current_key = key
            else:
                frontmatter_dict[key] = value
                current_key = None
        elif line.startswith('  - ') and current_key:
            # List item
            item = line[4:].strip()  # Remove '  - '
            if isinstance(frontmatter_dict[current_key], list):
                frontmatter_dict[current_key].append(item)

    # Join body content
    body_content = '\n'.join(lines[body_start:])

    return frontmatter_dict, body_content


def has_frontmatter(file_path):
    """Check if file already has frontmatter (starts with ---)."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            first_line = file.readline().strip()
            return first_line == '---'
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return True  # Assume it has frontmatter to avoid overwriting


def format_frontmatter_value(value):
    """Format a frontmatter value for output."""
    if isinstance(value, list):
        if len(value) == 0:
            return "[]"
        else:
            # Multi-line list format
            formatted = "\n"
            for item in value:
                formatted += f"  - {item}\n"
            return formatted.rstrip()
    else:
        return str(value)


def update_frontmatter(file_path):
    """Update existing frontmatter or add new frontmatter to the file."""
    # Get file info
    path = Path(file_path)
    file_name = path.stem  # filename without extension
    section_name = path.parent.name.lower()  # immediate parent directory
    created_date = get_creation_date(file_path)

    try:
        # Read existing content
        with open(file_path, 'r', encoding='utf-8') as file:
            existing_content = file.read()

        frontmatter_dict, body_content = parse_frontmatter(existing_content)

        if frontmatter_dict is None:
            # No existing frontmatter, add new one
            frontmatter_dict = {
                'tags': [section_name, CAMPAIGN_NAME],
                'date': created_date,
                'title': file_name,
                'author': [AUTHOR_NAME]
            }
        else:
            # Update existing frontmatter
            # Add title if not present
            if 'title' not in frontmatter_dict:
                frontmatter_dict['title'] = file_name

            # Set date field - use existing created_date if present, otherwise file creation date
            if 'created' in frontmatter_dict:
                frontmatter_dict['date'] = frontmatter_dict['created']
            elif 'date' not in frontmatter_dict:
                frontmatter_dict['date'] = created_date

        # Reconstruct frontmatter
        frontmatter_lines = ['---']

        # Preserve order: tags, date, title, author, then everything else
        ordered_keys = ['tags', 'date', 'title', 'author']

        for key in ordered_keys:
            if key in frontmatter_dict:
                value = frontmatter_dict[key]
                formatted_value = format_frontmatter_value(value)
                if '\n' in formatted_value:
                    frontmatter_lines.append(f'{key}:{formatted_value}')
                else:
                    frontmatter_lines.append(f'{key}: {formatted_value}')

        # Add any other keys that weren't in the ordered list
        for key, value in frontmatter_dict.items():
            if key not in ordered_keys:
                formatted_value = format_frontmatter_value(value)
                if '\n' in formatted_value:
                    frontmatter_lines.append(f'{key}:{formatted_value}')
                else:
                    frontmatter_lines.append(f'{key}: {formatted_value}')

        frontmatter_lines.append('---')

        # Combine frontmatter and body
        new_content = '\n'.join(frontmatter_lines) + '\n' + body_content

        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

        return True
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return False


def process_markdown_files():
    """Process all .md files in the current directory and subdirectories."""
    current_dir = Path('.')
    processed_files = []

    # Find all .md files
    md_files = list(current_dir.rglob('*.md'))

    if not md_files:
        print("No .md files found in the current directory and subdirectories.")
        return

    print(f"Found {len(md_files)} .md files. Processing...")
    print()

    for md_file in md_files:
        # Process all files (add frontmatter to new files, update existing ones)
        if update_frontmatter(md_file):
            processed_files.append(str(md_file))

            # Check what we did
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            frontmatter_dict, _ = parse_frontmatter(content)

            action = "Updated" if frontmatter_dict else "Added frontmatter to"
            print(f"Processed: {md_file}")

    print()
    if processed_files:
        print(f"Successfully processed {len(processed_files)} files:")
        for file_path in processed_files:
            print(f"  - {file_path}")
    else:
        print("No files were processed successfully.")


if __name__ == "__main__":
    print("Processing frontmatter in Obsidian markdown files...")
    print("=" * 50)

    # Verify we're in a campaign folder
    current_path = Path('.').resolve()
    if not any(d.startswith('0') for d in os.listdir('.') if os.path.isdir(d)):
        print(f"Warning: Current directory '{current_path.name}' doesn't look like a campaign vault.")
        print("Expected to find numbered directories (01 - session-notes, etc.).")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Exiting.")
            exit(1)

    process_markdown_files()
    print("\nDone!")
