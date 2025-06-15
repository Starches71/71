
import os
import subprocess
from datetime import datetime

def read_answer(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read().strip().lower()
    except:
        return ""

def git_setup_and_pull_with_stash():
    subprocess.run(["git", "config", "--global", "user.name", "github-actions[bot]"], check=True)
    subprocess.run(["git", "config", "--global", "user.email", "you@example.com"], check=True)
    
    # Stash all changes including untracked
    subprocess.run(["git", "stash", "--include-untracked"], check=True)
    
    # Pull latest changes with rebase
    subprocess.run(["git", "pull", "--rebase"], check=True)
    
    # Pop stash to restore local changes; ignore failure if nothing to pop
    subprocess.run(["git", "stash", "pop"], check=False)

def commit_file(commit_target):
    try:
        git_setup_and_pull_with_stash()

        os.makedirs("Vid", exist_ok=True)

        with open(commit_target, 'a', encoding='utf-8') as out:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            out.write(f"\n--- NEW ENTRY @ {timestamp} ---\n")
            for fname in ["tittle.txt", "view.txt", "yt_link"]:
                fpath = os.path.join("Vid", fname)
                if os.path.exists(fpath):
                    with open(fpath, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        out.write(f"{fname.upper().replace('.TXT','')}: {content}\n")

        subprocess.run(["git", "add", commit_target], check=True)

        result = subprocess.run(["git", "diff", "--cached", "--quiet"])
        if result.returncode != 0:
            subprocess.run(["git", "commit", "-m", f"Auto commit: {commit_target}"], check=True)
            subprocess.run(["git", "push"], check=True)
            print(f"✅ Committed: {commit_target}")
        else:
            print(f"ℹ️ No changes to commit for {commit_target}")

    except subprocess.CalledProcessError as e:
        print(f"❌ Commit failed: {e}")

def main():
    haram = read_answer("Vid/haram.txt")
    female = read_answer("Vid/female.txt")
    product = read_answer("Vid/product.txt")

    # STAGE ONE: Block if any are unsafe or not suitable
    if haram == "yes" or female == "yes" or product == "no":
        commit_file("AHARAM.txt")
        return

    # STAGE TWO: Process based on presence of person/music
    person = read_answer("Vid/person.txt")
    music = read_answer("Vid/music.txt")

    if person == "yes" and music == "yes":
        commit_file("AFACEMUSIC.txt")
    elif person == "yes":
        commit_file("AFACE.txt")
    elif music == "yes":
        commit_file("AMUSIC.txt")
    else:
        commit_file("AHALAL.txt")

if __name__ == "__main__":
    main()
