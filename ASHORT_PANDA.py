
# ASHORT_PANDA.py

import pandas as pd
import os

# File paths
yt_link_file = "Vid_yt_link.txt"
csv_output = "short_video_report.csv"
processed_links_file = "processed_links.txt"

# Read video link and title
with open(yt_link_file, "r") as f:
    link = f.readline().strip()
    title = f.readline().strip()

# Extract view count
views = title.split(" views ")[0].replace(",", "").strip()

# Function to read yes/no tags
def read_tag(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read().strip().lower()
    return "no"

# Tags
tags = {
    "haram": read_tag("Vid/haram.txt"),
    "female": read_tag("Vid/female.txt"),
    "person": read_tag("Vid/person.txt"),
    "music": read_tag("Vid/music.txt"),
    "product": read_tag("Vid/product.txt")
}

# New row
row = {
    "title": title,
    "link": link,
    "views": views,
    **tags
}

# Check if CSV exists and read it
if os.path.exists(csv_output):
    df = pd.read_csv(csv_output)
else:
    df = pd.DataFrame()

# Avoid duplicates
if (df["link"] == link).any():
    print("Already in CSV.")
else:
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(csv_output, index=False)
    print("Saved to CSV.")

# Update memory log
with open(processed_links_file, "a+") as f:
    f.seek(0)
    seen = f.read().splitlines()
    if link not in seen:
        f.write(link + "\n")
