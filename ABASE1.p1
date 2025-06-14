
import os
import subprocess

def read_answer(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read().strip().lower()
    except:
        return ""

def commit_file(commit_target):
    os.makedirs("Vid", exist_ok=True)
    with open(commit_target, 'w', encoding='utf-8') as out:
        for fname in ["tittle.txt", "view.txt", "yt_link"]:
            fpath = os.path.join("Vid", fname)
            if os.path.exists(fpath):
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    out.write(f"{fname.upper().replace('.TXT','')}: {content}\n")
    try:
        subprocess.run(["git", "config", "--global", "user.name", "github-actions[bot]"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "you@example.com"], check=True)
        subprocess.run(["git", "add", commit_target], check=True)
        subprocess.run(["git", "commit", "-m", f"Auto commit: {commit_target}"], check=True)
        subprocess.run(["git", "push"], check=True)
        print(f"Committed: {commit_target}")
    except subprocess.CalledProcessError as e:
        print(f"Commit failed: {e}")

def main():
    # Step 1: Check haram, female, product
    haram = read_answer("Vid/haram.txt")
    female = read_answer("Vid/female.txt")
    product = read_answer("Vid/product.txt")

    if "yes" in (haram, female, product):
        commit_file("AHARAM.txt")
        return

    # Step 2: Check person and music
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
