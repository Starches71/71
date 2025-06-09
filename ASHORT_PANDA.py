
import pandas as pd

# === STEP 1: Read the TXT file ===
with open("VID_SHORT_ooo.txt", "r", encoding="utf-8") as f:
    lines = f.read().splitlines()

# === STEP 2: Extract video data ===
videos = []
for i in range(0, len(lines), 2):
    views_title = lines[i]
    link = lines[i + 1]

    # Extract view count (first part before 'views')
    views, title = views_title.split(' views | ', 1)
    views = views.replace(",", "").strip()

    videos.append({
        "Title": title.strip(),
        "Views": int(views),
        "Link": link.strip()
    })

# === STEP 3: Load detection flags ===
def load_flag(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [x.strip().lower() for x in f.readlines()]
    except FileNotFoundError:
        return ["no"] * len(videos)

haram_flags = load_flag("Vid/haram.txt")
female_flags = load_flag("Vid/female.txt")
person_flags = load_flag("Vid/person.txt")
music_flags = load_flag("Vid/music.txt")
product_flags = load_flag("Vid/product.txt")

# === STEP 4: Add flags to videos ===
for i in range(len(videos)):
    videos[i]["Haram"] = haram_flags[i]
    videos[i]["Female"] = female_flags[i]
    videos[i]["Person"] = person_flags[i]
    videos[i]["Music"] = music_flags[i]
    videos[i]["Product"] = product_flags[i]

# === STEP 5: Create DataFrame and save as CSV ===
df = pd.DataFrame(videos)
df.to_csv("short_video_report.csv", index=False)
print("✅ Report saved as short_video_report.csv")
