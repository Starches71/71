
import os
import re
from pathlib import Path
from datetime import datetime

# Paths
short_file = Path("VID_SHORT_ooo.txt")
used_links_file = Path("Vid/yt_link")
output_file = Path("ASHORT.txt")

# Ensure directory exists
used_links_file.parent.mkdir(parents=True, exist_ok=True)

# Load already used links
used_links = set()
if used_links_file.exists():
    used_links = set(used_links_file.read_text().splitlines())

# Read blocks from the main file
with short_file.open("r", encoding="utf-8") as f:
    lines = f.read().splitlines()

# Find and process blocks
block = []
for i in range(0, len(lines), 2):
    if i + 1 >= len(lines):
        continue  # Skip incomplete block
    title = lines[i]
    link = lines[i + 1].strip()

    if link in used_links:
        continue  # Already used

    block = [title, link]
    break

if not block:
    print("❌ No new blocks found.")
    exit(0)

# Append to ASHORT.txt
with output_file.open("a", encoding="utf-8") as out:
    out.write("\n".join(block) + "\n\n")

# Append to yt_link
with used_links_file.open("a", encoding="utf-8") as yt:
    yt.write(block[1] + "\n")

# Git commit and push
commit_message = f"Used new short block - {datetime.utcnow().isoformat()}"

os.system("git add ASHORT.txt Vid/yt_link")
os.system("git config user.name 'github-actions[bot]'")
os.system("git config user.email 'github-actions[bot]@users.noreply.github.com'")
os.system("git commit -m '{}'".format(commit_message))
os.system("git pull --rebase origin main")
os.system("git push origin main")

print("✅ Block used and committed")
