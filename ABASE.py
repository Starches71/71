
import os
import re
import subprocess
from datetime import datetime

def extract_video_info():
    # Paths
    input_file = "VID_SHORT_ooo.txt"
    base_dir = "Vid"
    os.makedirs(base_dir, exist_ok=True)

    used_file = "Aused.txt"  # Memory file for used links
    title_path = os.path.join(base_dir, "tittle.txt")
    view_path = os.path.join(base_dir, "view.txt")
    link_path = os.path.join(base_dir, "yt_link")

    # Load used links from Aused.txt
    used_links = set()
    if os.path.exists(used_file):
        with open(used_file, 'r', encoding='utf-8') as f:
            used_links = set(line.strip() for line in f if line.strip())

    # Read all input lines
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    for i in range(0, len(lines), 2):
        try:
            info_line = lines[i]
            url_line = lines[i + 1]

            if url_line in used_links:
                continue

            match = re.match(r"([\d,]+) views \| (.+)", info_line)
            if not match:
                continue

            views = match.group(1).replace(",", "")
            title = match.group(2)
            link = url_line

            # Save data
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

            # 🔁 COMMIT the update to GitHub
            commit_changes()

            return

        except IndexError:
            continue

    print("\n⚠️ No new links found.")

def commit_changes():
    print("\n📦 Committing changes to GitHub...")
    try:
        subprocess.run(['git', 'config', '--global', 'user.name', 'yt-bot'], check=True)
        subprocess.run(['git', 'config', '--global', 'user.email', 'yt-bot@example.com'], check=True)

        subprocess.run(['git', 'stash', '--include-untracked'], check=True)
        subprocess.run(['git', 'pull', '--rebase', 'origin', 'main'], check=True)
        subprocess.run(['git', 'stash', 'pop'], check=True)

        # Stage files — customize this pattern if needed
        subprocess.run(['git', 'add', 'Aused.txt'], check=True)

        # Commit only if there are changes
        result = subprocess.run(['git', 'diff', '--cached', '--quiet'])
        if result.returncode != 0:
            msg = f"✅ Update Aused.txt - {datetime.utcnow().isoformat()}"
            subprocess.run(['git', 'commit', '-m', msg], check=True)
            subprocess.run(['git', 'push'], check=True)
            print("✅ Changes committed and pushed.")
        else:
            print("ℹ️ No changes to commit.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Git commit failed: {e}")

if __name__ == "__main__":
    extract_video_info()
