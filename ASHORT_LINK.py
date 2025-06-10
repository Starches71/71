
import os

# Paths
INPUT_FILE = "VID_SHORT_ooo.txt"
VID_DIR = "Vid"
TITLE_FILE = os.path.join(VID_DIR, "tittle")
YT_LINK_FILE = os.path.join(VID_DIR, "yt_link")

# Make Vid directory if it doesn't exist
os.makedirs(VID_DIR, exist_ok=True)

# Read all lines from input file
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Load all already seen links from marked lines
seen_links = set()
for i in range(0, len(lines) - 1, 3):
    title = lines[i].strip()
    url = lines[i+1].strip()
    if title.startswith("□"):
        seen_links.add(url)

# Search for first new unprocessed link
i = 0
while i < len(lines) - 1:
    title_line = lines[i].strip()
    url_line = lines[i+1].strip()

    # Skip if already marked
    if title_line.startswith("□") or url_line in seen_links:
        i += 3
        continue

    print(f"Found new link: {url_line}")
    
    # Save title and link
    with open(TITLE_FILE, 'w') as tf:
        tf.write(title_line)
    with open(YT_LINK_FILE, 'w') as lf:
        lf.write(url_line)

    # Mark this block as processed
    lines[i] = "□" + title_line + "\n"
    seen_links.add(url_line)
    break  # Stop after finding the first new one

    i += 3

# Save updated input file
with open(INPUT_FILE, 'w', encoding='utf-8') as f:
    f.writelines(lines)
