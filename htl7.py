
import os
import subprocess
import time

# Directory paths
links_dir = "best_link"
output_dir = "best_vid"

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

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

# Iterate through each .links.txt file in the links directory
for links_file in os.listdir(links_dir):
    if links_file.endswith('.links.txt'):
        file_path = os.path.join(links_dir, links_file)

        # Read all links from the current file
        with open(file_path, 'r') as f:
            links = f.readlines()

        # For each link, download the video using yt-dlp with Tor
        for idx, link in enumerate(links):
            link = link.strip()
            if not link:
                continue  # Skip empty lines

            # Construct output filename
            suffix = chr(65 + idx)  # Converts 0 to 'A', 1 to 'B', etc.
            output_filename = f"{links_file.split('.')[0]}{suffix}.mp4"
            output_filepath = os.path.join(output_dir, output_filename)

            print(f"[INFO] Downloading {link} as {output_filename} via Tor...")

            # Use yt-dlp with Tor proxy
            cmd = [
                "yt-dlp",
                "--proxy", "socks5://127.0.0.1:9050",
                "-f", "bestvideo+bestaudio",
                "-o", output_filepath,
                link
            ]
            subprocess.run(cmd)

            # Delay to prevent detection
            time.sleep(2)

print("[INFO] All downloads completed successfully.")
