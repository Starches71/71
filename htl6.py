
import os
import subprocess
import traceback

# Paths
descriptions_dir = "best_descriptions"
places_dir = "places"
links_dir = "best_link"

# Ensure the links directory exists
os.makedirs(links_dir, exist_ok=True)

# Read the place name from "places.txt"
try:
    with open(os.path.join(places_dir, "places.txt"), "r") as f:
        place_name = f.readline().strip()
    print(f"Place name extracted: {place_name}")
except Exception as e:
    print(f"Error reading 'places.txt': {e}")
    exit(1)

# List hotel description files
hotel_files = os.listdir(descriptions_dir)
if not hotel_files:
    print(f"No files found in directory: {descriptions_dir}")
    exit(1)

# Function to fetch video links using yt-dlp
def fetch_video_links(search_query, max_results=3):
    try:
        command = [
            "yt-dlp", f"ytsearch{max_results}:{search_query}", 
            "--print", "%(webpage_url)s"
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        video_urls = result.stdout.strip().split("\n")
        return video_urls if video_urls else None
    except Exception as e:
        print(f"Error fetching video links: {e}")
        return None

# Process each hotel file
for hotel_file in hotel_files:
    try:
        hotel_name = hotel_file.split('.')[1].strip()
        search_query = f"{hotel_name} {place_name}"
        print(f"Searching for: {search_query}")

        video_urls = fetch_video_links(search_query)
        if not video_urls:
            print(f"No video links found for {hotel_name}")
            continue

        # Save video URLs
        links_file_path = os.path.join(links_dir, f"{hotel_file.split('.')[0]}.links.txt")
        with open(links_file_path, "w") as links_file:
            for url in video_urls:
                links_file.write(url + '\n')
        print(f"Fetched URLs for {hotel_name} and saved to {links_file_path}")

    except Exception as e:
        print(f"Error processing {hotel_file}: {e}")
        traceback.print_exc()
