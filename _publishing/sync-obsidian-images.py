"""
Sync Obsidian Images to Hugo
==============================
Converts Obsidian image embed syntax (![[image.png]]) to standard markdown
(![ ](url)) and copies the image files from the Obsidian attachments folder
to the Hugo static/images/ directory.

Run after convert_wikilinks.py (or via update.sh which does both in order).

Usage:
    python sync-obsidian-images.py
"""

# ===========================================================================
# CONFIG — update these paths before running
# ===========================================================================
CONTENT_DIR       = "/path/to/hugo-site/content/"
# Path to your Obsidian attachments folder (where images are stored in Obsidian)
ATTACHMENTS_DIR   = "/path/to/obsidian/attachments/"
STATIC_IMAGES_DIR = "/path/to/hugo-site/static/images/"
# ===========================================================================

import os
import re
import shutil


# Step 1: Process each markdown file in the content directory (recursively)
for root, dirs, files in os.walk(CONTENT_DIR):
    for filename in files:
        if filename.endswith(".md"):
            filepath = os.path.join(root, filename)

            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()

            # Step 2: Find all image embeds in Obsidian format: ![[image.png]] or ![[image.png|size]]
            images = re.findall(r'!\[\[([^]]*\.(jpe?g|png|gif|bmp|webp))(\|[^\]]*)?\]\]', content)

            # Step 3: Replace image embeds with standard markdown links
            for image_tuple in images:
                image = image_tuple[0]
                size_spec = image_tuple[2] if len(image_tuple) > 2 else ""

                # Original Obsidian format to search for
                original_obsidian = f"![[{image}{size_spec}]]"

                # Standard markdown link (spaces → %20 in URL; size spec is dropped)
                markdown_image = f"![{image}](/images/{image.replace(' ', '%20')})"
                content = content.replace(original_obsidian, markdown_image)
                print(f"Processing: {filename}")
                print(f"  -> Image: {image}")

                # Step 4: Copy the image file to Hugo static/images/ if it exists
                image_source = os.path.join(ATTACHMENTS_DIR, image)
                if os.path.exists(image_source):
                    shutil.copy(image_source, STATIC_IMAGES_DIR)
                else:
                    print(f"  Warning: image not found at {image_source}")

            # Step 5: Write the updated content back to the markdown file
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(content)

print("Markdown files processed and images copied successfully.")
