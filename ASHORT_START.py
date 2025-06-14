
import os
import subprocess
from datetime import datetime

SOURCE_FILE = "VID_SHORT_ooo.txt"
USED_LINKS_FILE = "ASHORT.txt"
OUTPUT_LINK_FILE = "vid/yt_link"

def load_used_links():
    if not os.path.exists(USED_LINKS_FILE):
        return set()
    with open(USED_LINKS_FILE, "r") as f:
        return set(line.strip() for line in f if line.strip())

def save_used_link(link):
    with open(USED_LINKS_FILE, "a") as f:
        f.write(link + "\n")

def get_next_unused_link():
    if not os.path.exists(SOURCE_FILE):
        raise FileNotFoundError(f"{SOURCE_FILE} not found.")

    with open(SOURCE_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    used_links = load_used_links()

    # The file has alternating lines: description, then link
    for i in range(1, len(lines), 2):
        link = lines[i]
        if link not in used_links:
            return lines[i - 1], link  # (description, link)

    return None, None

def save_link_to_file(link):
    os.makedirs(os.path.dirname(OUTPUT_LINK_FILE), exist_ok=True)
    with open(OUTPUT_LINK_FILE, "w") as f:
        f.write(link)

def git_commit_changes():
    subprocess.run(["git", "config", "--global", "user.name", "yt-bot"], check=True)
    subprocess.run(["git", "config", "--global", "user.email", "yt-bot@example.com"], check=True)

    # Stage files first
    subprocess.run(["git", "add", USED_LINKS_FILE, OUTPUT_LINK_FILE], check=True)

    # Check if there is anything to commit
    result = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if result.returncode == 0:
        print("✅ No changes to commit.")
        return

    # Commit the changes
    commit_msg = f"Auto-save used link - {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)

    # Now pull with rebase (safe after committing)
    subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=True)

    # Push changes
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("✅ Changes committed and pushed.")

def main():
    desc, link = get_next_unused_link()
    if not link:
        print("✅ All links have been used.")
        return

    print(f"🎯 Selected: {link}")
    save_link_to_file(link)
    save_used_link(link)
    git_commit_changes()

if __name__ == "__main__":
    main()
