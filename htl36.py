import os
import subprocess
import time
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
    print(f"[INFO] Place name extracted: {place_name}")
except Exception as e:
    print(f"[ERROR] Could not read 'places.txt': {e}")
    exit(1)

# List hotel description files
hotel_files = os.listdir(descriptions_dir)
if not hotel_files:
    print(f"[ERROR] No files found in directory: {descriptions_dir}")
    exit(1)

# Start Tor as a background process
print("[INFO] Starting Tor service...")
subprocess.run(["tor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Wait a few seconds for Tor to establish a connection
time.sleep(5)

# Check Tor exit node IP
print("[INFO] Checking Tor exit node IP...")
tor_ip_check = subprocess.run(["curl", "--socks5", "127.0.0.1:9050", "https://check.torproject.org/api/ip"], capture_output=True, text=True)
print(f"[INFO] Tor IP: {tor_ip_check.stdout.strip()}")

# Resolve YouTube domain through Tor
print("[INFO] Resolving youtube.com via Tor...")
subprocess.run(["curl", "--socks5", "127.0.0.1:9050", "https://dns.google.com/resolve?name=www.youtube.com&type=A"], stdout=subprocess.DEVNULL)

# Function to fetch video links using yt-dlp via Tor
def fetch_video_links(search_query, max_results=3):
    try:
        command = [
            "yt-dlp", "--proxy", "socks5://127.0.0.1:9050", 
            f"ytsearch{max_results}:{search_query}", "--print", "%(webpage_url)s"
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        video_urls = result.stdout.strip().split("\n")
        return video_urls if video_urls else None
    except Exception as e:
        print(f"[ERROR] Failed to fetch video links: {e}")
        return None

# Process each hotel file
for hotel_file in hotel_files:
    try:
        hotel_name = hotel_file.split('.')[1].strip()
        search_query = f"{hotel_name} {place_name}"
        print(f"[INFO] Searching for: {search_query}")

        video_urls = fetch_video_links(search_query)
        if not video_urls:
            print(f"[WARNING] No video links found for {hotel_name}")
            continue

        # Save video URLs
        links_file_path = os.path.join(links_dir, f"{hotel_file.split('.')[0]}.links.txt")
        with open(links_file_path, "w") as links_file:
            for url in video_urls:
                links_file.write(url + '\n')
        print(f"[INFO] Fetched URLs for {hotel_name} and saved to {links_file_path}")

    except Exception as e:
        print(f"[ERROR] Error processing {hotel_file}: {e}")
        traceback.print_exc()

print("[INFO] Video link search completed successfully.")
