
import os
import re

def extract_video_info():
    # Paths
    input_file = "VID_SHORT_ooo.txt"
    base_dir = "Vid"
    os.makedirs(base_dir, exist_ok=True)

    link_path = os.path.join(base_dir, "link.txt")
    title_path = os.path.join(base_dir, "tittle.txt")
    view_path = os.path.join(base_dir, "view.txt")

    # Temp memory (simulate env variable or memory-based storage)
    seen_links = set()

    # If already processed links exist in link.txt, load them
    if os.path.exists(link_path):
        with open(link_path, 'r', encoding='utf-8') as f:
            seen_links = set(line.strip() for line in f if line.strip())

    # Temp storage for new items
    new_links, new_titles, new_views = [], [], []

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    for i in range(0, len(lines), 2):
        try:
            # Line with views and title
            info_line = lines[i]
            url_line = lines[i + 1]

            # Skip if already processed
            if url_line in seen_links:
                continue

            # Extract view count
            match = re.match(r"([\d,]+) views \| (.+)", info_line)
            if not match:
                continue

            views = match.group(1).replace(",", "")
            title = match.group(2)
            link = url_line

            # Add to memory
            seen_links.add(link)
            new_links.append(link)
            new_titles.append(title)
            new_views.append(views)

        except IndexError:
            continue  # In case of unmatched lines

    # Write new data (just for this session – optional in GH Actions)
    with open(link_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(new_links))
    with open(title_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(new_titles))
    with open(view_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(new_views))

    print(f"\n✅ Extracted {len(new_links)} new entries.")
    print(f"First title: {new_titles[0] if new_titles else 'None'}")
    print(f"First link: {new_links[0] if new_links else 'None'}")
    print(f"First views: {new_views[0] if new_views else 'None'}")

if __name__ == "__main__":
    extract_video_info()
