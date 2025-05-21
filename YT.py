
import os
import re
from groq import Groq

# Load API key
GROQ_API_KEY = os.getenv("GROQ_API")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API key is missing. Please set it as an environment variable.")
client = Groq(api_key=GROQ_API_KEY)

# Paths
MERGED_FILE = "VID_LONG_MERGED.txt"
VID_DIR = "Vid"
TITLE_FILE = os.path.join(VID_DIR, "tittle")
YT_LINK_FILE = os.path.join(VID_DIR, "yt_link")

# Make Vid directory if it doesn't exist
os.makedirs(VID_DIR, exist_ok=True)

# Function to check niche via Groq
def is_tech_niche(title):
    prompt = f"Is this YouTube video title related to tech, gadgets, unboxing, or product reviews? Just answer yes or no:\n\n\"{title}\""
    try:
        response = client.chat.completions.create(
            model="Llama-3-3-70b-Versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=5,
        )
        answer = response.choices[0].message.content.strip().lower()
        return "yes" in answer
    except Exception as e:
        print(f"Groq error: {e}")
        return False

# Read all lines from merged file
with open(MERGED_FILE, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Search for first unmarked block that matches the pattern
i = 0
while i < len(lines) - 1:
    title_line = lines[i].strip()
    url_line = lines[i+1].strip()

    if title_line.startswith("□"):
        i += 3  # Skip to next block
        continue

    print(f"Checking: {title_line}")
    if is_tech_niche(title_line):
        print("This is a tech niche video. Saving title and link...")
        with open(TITLE_FILE, 'w') as tf:
            tf.write(title_line)
        with open(YT_LINK_FILE, 'w') as lf:
            lf.write(url_line)
        break
    else:
        print("Not tech niche. Marking and continuing...")
        lines[i] = "□" + title_line + "\n"
        i += 3

# Save updated merged file
with open(MERGED_FILE, 'w', encoding='utf-8') as f:
    f.writelines(lines)
