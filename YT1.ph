
import subprocess
import os
import time
import sys

# === UTILITIES ===
def run_command(command, error_msg, retries=1, delay=5):
    for attempt in range(retries):
        try:
            subprocess.run(command, check=True)
            return
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] {error_msg} (Attempt {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                print(f"[*] Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("[✘] Exiting due to repeated failures.")
                sys.exit(1)

# === SETUP TOR ===
def start_tor():
    print("[*] Setting up Tor...")

    # Check if Tor is installed
    tor_installed = subprocess.run(["which", "tor"], capture_output=True).returncode == 0
    if not tor_installed:
        print("[*] Installing Tor...")
        run_command(["sudo", "apt-get", "update"], "Failed to update package list", retries=2)
        run_command(["sudo", "apt-get", "install", "-y", "tor"], "Failed to install Tor", retries=2)

    print("[*] Starting Tor service...")
    run_command(["sudo", "service", "tor", "start"], "Failed to start Tor", retries=2)

    # Optional: check if Tor is working
    try:
        result = subprocess.run(
            ["curl", "--socks5", "127.0.0.1:9050", "https://check.torproject.org/"],
            capture_output=True,
            timeout=10,
        )
        if b"Congratulations" in result.stdout:
            print("[✓] Tor is active.")
        else:
            print("[!] Warning: Tor check did not return confirmation.")
    except Exception as e:
        print(f"[!] Skipping Tor validation due to error: {e}")

# === READ LINK ===
def read_youtube_link(file_path):
    try:
        with open(file_path, "r") as f:
            link = f.read().strip()
            if not link:
                raise ValueError("YouTube link file is empty.")
            return link
    except Exception as e:
        print(f"[ERROR] Could not read YouTube link: {e}")
        sys.exit(1)

# === DOWNLOAD FULL VIDEO (Video + Audio) ===
def download_full_video(link, out_dir):
    print("[*] Downloading full video with audio...")
    run_command([
        "yt-dlp",
        "--proxy", "socks5://127.0.0.1:9050",
        "-f", "best",
        "-o", os.path.join(out_dir, "video.%(ext)s"),
        link
    ], "Video download failed", retries=3, delay=7)

# === MAIN FLOW ===
if __name__ == "__main__":
    link_file = "Vid/yt_link"
    output_dir = "Vid"

    os.makedirs(output_dir, exist_ok=True)

    start_tor()
    yt_url = read_youtube_link(link_file)
    print(f"[*] Downloading from: {yt_url}")

    download_full_video(yt_url, output_dir)

    print("[✓] Download complete.")
