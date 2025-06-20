
import os
import re
import subprocess
from datetime import datetime

def extract_asmr_link():
    input_file = "ASMR_SHORT.txt"
    used_file = "ASMR_USED.txt"
    link_path = os.path.join("Vid", "yt_link")
    os.makedirs("Vid", exist_ok=True)

    used_links = set()
    if os.path.exists(used_file):
        with open(used_file, 'r', encoding='utf-8') as f:
            used_links = set(line.strip() for line in f if line.strip())

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    for i in range(len(lines) - 1):
        info_line = lines[i]
        link_line = lines[i + 1]

        if not link_line.startswith("https://www.youtube.com/watch?v="):
            continue
        if link_line in used_links:
            continue

        with open(link_path, 'w', encoding='utf-8') as f:
            f.write(link_line)

        with open(used_file, 'a', encoding='utf-8') as f:
            f.write(link_line + "\n")

        print("\n✅ New ASMR link found and saved:")
        print("Link:", link_line)

        commit_changes(used_file)
        return

    print("\n⚠️ No new valid links found.")

def commit_changes(file_to_commit):
    print("\n📦 Committing changes to GitHub...")
    try:
        subprocess.run(['git', 'config', '--global', 'user.name', 'yt-bot'], check=True)
        subprocess.run(['git', 'config', '--global', 'user.email', 'yt-bot@example.com'], check=True)

        subprocess.run(['git', 'stash', '--include-untracked'], check=True)
        subprocess.run(['git', 'pull', '--rebase', 'origin', 'main'], check=True)
        subprocess.run(['git', 'stash', 'pop'], check=True)

        subprocess.run(['git', 'add', file_to_commit], check=True)

        result = subprocess.run(['git', 'diff', '--cached', '--quiet'])
        if result.returncode != 0:
            msg = f"✅ Update {file_to_commit} - {datetime.utcnow().isoformat()}"
            subprocess.run(['git', 'commit', '-m', msg], check=True)
            subprocess.run(['git', 'push'], check=True)
            print("✅ Changes committed and pushed.")
        else:
            print("ℹ️ No changes to commit.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Git commit failed: {e}")

if __name__ == "__main__":
    extract_asmr_link()
