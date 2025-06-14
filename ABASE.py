
import os
import re

def extract_video_info():
    # Paths
    input_file = "VID_SHORT_ooo.txt"
    base_dir = "Vid"
    os.makedirs(base_dir, exist_ok=True)

    used_file = "Aused.txt"  # NEW: memory file for used links
    title_path = os.path.join(base_dir, "tittle.txt")
    view_path = os.path.join(base_dir, "view.txt")
    link_path = os.path.join(base_dir, "yt_link")  # save current link

    # Load used links from Aused.txt
    used_links = set()
    if os.path.exists(used_file):
        with open(used_file, 'r', encoding='utf-8') as f:
            used_links = set(line.strip() for line in f if line.strip())

    # Read all input lines
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    # Go line by line (2 lines at a time)
    for i in range(0, len(lines), 2):
        try:
            info_line = lines[i]
            url_line = lines[i + 1]

            # Skip if already used
            if url_line in used_links:
                continue

            # Match "123 views | Title"
            match = re.match(r"([\d,]+) views \| (.+)", info_line)
            if not match:
                continue

            views = match.group(1).replace(",", "")
            title = match.group(2)
            link = url_line

            # Write to individual files (only 1 entry)
            with open(link_path, 'w', encoding='utf-8') as f:
                f.write(link)
            with open(title_path, 'w', encoding='utf-8') as f:
                f.write(title)
            with open(view_path, 'w', encoding='utf-8') as f:
                f.write(views)
            with open(used_file, 'a', encoding='utf-8') as f:
                f.write(link + "\n")

            print("\n✅ 1 new video extracted:")
            print("Title:", title)
            print("Link:", link)
            print("Views:", views)
            return  # Stop after 1 new link is processed

        except IndexError:
            continue

    print("\n⚠️ No new links found.")

if __name__ == "__main__":
    extract_video_info()
