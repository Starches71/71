
import os

# Paths
vid_dir = "Vid"
description_file = os.path.join(vid_dir, "Description.txt")
links_file = os.path.join(vid_dir, "links.txt")
final_description_file = os.path.join(vid_dir, "final_description.txt")

# Check if files exist
if not os.path.exists(description_file):
    print(f"❌ File not found: {description_file}")
    exit()

if not os.path.exists(links_file):
    print(f"❌ File not found: {links_file}")
    exit()

# Read the description and links
with open(description_file, "r", encoding="utf-8") as f:
    description_content = f.read()

with open(links_file, "r", encoding="utf-8") as f:
    links_content = f.read()

# Combine links first, then description
final_content = f"{links_content}\n\n{description_content}"

# Save the final combined description
with open(final_description_file, "w", encoding="utf-8") as f:
    f.write(final_content)

print(f"✅ Combined description saved to: {final_description_file}")
