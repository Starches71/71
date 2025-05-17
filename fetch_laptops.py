
# .github/scripts/fetch_laptops.py
import requests, os
from datetime import datetime, timedelta

API_KEY = os.getenv("YT_API_KEY")
MAX_RESULTS = 50
TOTAL_RESULTS = 200
QUERY = "laptop unboxing"

shorts_file = "VID_short_lp.txt"
long_file = "VID_long_lp.txt"

now = datetime.utcnow()
start_of_week = now - timedelta(days=now.weekday())
published_after = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"

seen_ids = set()
for file in [shorts_file, long_file]:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                if 'youtube.com/watch?v=' in line:
                    vid = line.strip().split('watch?v=')[1]
                    seen_ids.add(vid)

all_items = []
next_page = ""

for _ in range(TOTAL_RESULTS // MAX_RESULTS):
    search_url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?part=snippet"
        f"&q={QUERY}"
        f"&maxResults={MAX_RESULTS}"
        f"&order=viewCount"
        f"&publishedAfter={published_after}"
        f"&type=video"
        f"&videoLicense=creativeCommon"
        f"&key={API_KEY}"
    )
    if next_page:
        search_url += f"&pageToken={next_page}"

    resp = requests.get(search_url)
    data = resp.json()
    video_ids = [item['id']['videoId'] for item in data.get('items', [])]
    next_page = data.get("nextPageToken", "")

    if not video_ids:
        break

    stats_url = (
        f"https://www.googleapis.com/youtube/v3/videos"
        f"?part=contentDetails,statistics,snippet"
        f"&id={','.join(video_ids)}"
        f"&key={API_KEY}"
    )
    stats_resp = requests.get(stats_url)
    stats_data = stats_resp.json()

    for vid in stats_data.get("items", []):
        vid_id = vid["id"]
        if vid_id in seen_ids:
            continue
        seen_ids.add(vid_id)

        duration = vid["contentDetails"]["duration"]
        views = int(vid["statistics"].get("viewCount", 0))
        title = vid["snippet"]["title"].replace('\n', ' ').strip()
        link = f"https://www.youtube.com/watch?v={vid_id}"

        # Rough check for short
        is_short = "M" not in duration and "S" in duration

        entry = f"{views:,} views | {title}\n{link}\n\n"
        all_items.append((views, entry, is_short))

shorts = sorted([e for v, e, s in all_items if s], reverse=True)
longs = sorted([e for v, e, s in all_items if not s], reverse=True)

with open(shorts_file, 'a+', encoding='utf-8') as f:
    f.seek(0)
    existing = f.read()
    for item in shorts:
        if item not in existing:
            f.write(item)

with open(long_file, 'a+', encoding='utf-8') as f:
    f.seek(0)
    existing = f.read()
    for item in longs:
        if item not in existing:
            f.write(item)
