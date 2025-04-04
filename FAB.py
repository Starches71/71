

import os
import requests
from datetime import datetime, timedelta

# Facebook credentials
ACCESS_TOKEN = "EAAYaCBvT83UBOziasqgAPPHaNQHZCYZCW4B9dMNNDJbRwn1rrSmoeauxd6ERTXNZBCivKt2rDpkFSBiQIP99offXoGSyvCC3sdRqXRi2FgRqmYoZBxVRUOSrFUbkZADZB9MlCeUdw6DwN0fPWryEzZBfaREp6tepfZA8r0j7DYMZCZCDuMwK8x1G4vU4OwvPdOP7IeuM3ltRTQ"
BASE_URL = "https://graph.facebook.com/v19.0"

# Facebook pages to scan
PAGES = {
    "MKBHD": "MarquesBrownlee",
    "The Verge": "verge",
    "Tech Insider": "techinsider",
    "Linus Tech Tips": "linustechtips",
    "Unbox Therapy": "UnboxTherapy",
    "Digital Trends": "digitaltrends",
    "Gadget Flow": "thegadgetflow",
    "NowThis Future": "NowThisFuture",
    "TWiT Network": "TWiTNetwork",
    "ShortCircuit": "ShortCircuitYT",
    "Fossbytes": "fossbytes"
}

# How recent to fetch
TIME_WINDOW_HOURS = 12

# Output directory
OUTPUT_DIR = "fb"

def ensure_directory():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def count_existing_files():
    return len([f for f in os.listdir(OUTPUT_DIR) if f.startswith("post") and f.endswith(".txt")])

def fetch_recent_text_posts(page_name):
    url = f"{BASE_URL}/{page_name}/posts"
    params = {
        "access_token": ACCESS_TOKEN,
        "fields": "message,created_time",
        "limit": 10
    }
    res = requests.get(url, params=params)
    if res.status_code != 200:
        print(f"Error fetching from {page_name}: {res.text}")
        return []

    posts = res.json().get("data", [])
    time_cutoff = datetime.utcnow() - timedelta(hours=TIME_WINDOW_HOURS)

    filtered = []
    for post in posts:
        message = post.get("message", "")
        created = datetime.strptime(post['created_time'], "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)
        if created >= time_cutoff and "video" not in message.lower() and "youtu" not in message.lower():
            filtered.append(message)
    return filtered

def save_posts_to_files(posts, start_index=1):
    index = start_index
    for post in posts:
        filename = os.path.join(OUTPUT_DIR, f"post{index}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(post.strip())
        print(f"Saved: {filename}")
        index += 1

def main():
    ensure_directory()
    file_start = count_existing_files() + 1
    total_collected = 0

    for label, page in PAGES.items():
        print(f"Fetching from: {label}")
        posts = fetch_recent_text_posts(page)
        if posts:
            save_posts_to_files(posts, start_index=file_start)
            file_start += len(posts)
            total_collected += len(posts)

    if total_collected == 0:
        print("No fresh plain text posts found.")

if __name__ == "__main__":
    main()
