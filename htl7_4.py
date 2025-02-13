import os
import subprocess
import time

# Directory paths
places_dir = "places"
output_dir = "best_vid"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Start Tor as a background process
def start_tor():
    print("[INFO] Starting Tor service...")
    tor_process = subprocess.Popen(["tor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(10)

# Check Tor exit node IP
def check_tor_ip():
    print("[INFO] Checking Tor exit node IP...")
    tor_ip_check = subprocess.run(["curl", "--socks5", "127.0.0.1:9050", "https://check.torproject.org/api/ip"], capture_output=True, text=True)
    print(f"[INFO] Tor IP: {tor_ip_check.stdout.strip()}")

# Resolve YouTube domain through Tor
def resolve_youtube():
    print("[INFO] Resolving youtube.com via Tor...")
    subprocess.run(["curl", "--socks5", "127.0.0.1:9050", "https://dns.google.com/resolve?name=www.youtube.com&type=A"], stdout=subprocess.DEVNULL)

# Process hotel from the 2nd line in places directory
hotel_file = os.path.join(places_dir, "hotel4.txt")
with open(hotel_file, "r") as f:
    hotels = [line.strip() for line in f.readlines() if line.strip()]

for hotel in hotels:
    print(f"[INFO] Searching YouTube for: {hotel}")

    # Search YouTube for three video links
    search_cmd = [
        "yt-dlp",
        "--proxy", "socks5://127.0.0.1:9050",
        f"ytsearch3:{hotel}",
        "--print", "%(webpage_url)s"
    ]
    result = subprocess.run(search_cmd, capture_output=True, text=True)
    video_links = result.stdout.strip().split("\n")

    # Download each video
    for idx, link in enumerate(video_links):
        if not link:
            continue  # Skip empty results

        suffix = chr(65 + idx)  # A, B, C
        output_filename = f"{hotel.replace(' ', '_')}{suffix}.mp4"
        output_filepath = os.path.join(output_dir, output_filename)

        print(f"[INFO] Downloading {link} as {output_filename} via Tor...")

        # Download video with retry mechanism
        max_attempts = 5
        attempt = 1

        while attempt <= max_attempts:
            cmd = [
                "yt-dlp",
                "--proxy", "socks5://127.0.0.1:9050",
                "-f", "bestvideo+bestaudio",
                "--merge-output-format", "mp4",
                "-o", output_filepath,
                link
            ]
            result = subprocess.run(cmd)

            if result.returncode == 0:
                print(f"[INFO] Successfully downloaded: {output_filename}")
                break
            else:
                print(f"[ERROR] Failed attempt {attempt} for {link}. Retrying...")
                attempt += 1

                # Restart Tor to get a new IP
                print("[INFO] Restarting Tor for a new IP...")
                subprocess.run(["pkill", "-HUP", "tor"])
                time.sleep(10)  # Wait for a new Tor circuit

                # Check new Tor IP
                tor_ip_check = subprocess.run(["curl", "--socks5", "127.0.0.1:9050", "https://check.torproject.org/api/ip"], capture_output=True, text=True)
                print(f"[INFO] New Tor IP: {tor_ip_check.stdout.strip()}")

        if attempt > max_attempts:
            print(f"[ERROR] Failed to download {link} after {max_attempts} attempts.")

    # Small delay to avoid detection
    time.sleep(2)

print("[INFO] All downloads completed successfully.")
