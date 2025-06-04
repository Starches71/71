
import subprocess
import os
import time
import sys
import glob

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

    tor_installed = subprocess.run(["which", "tor"], capture_output=True).returncode == 0
    if not tor_installed:
        print("[*] Installing Tor...")
        run_command(["sudo", "apt-get", "update"], "Failed to update package list", retries=2)
        run_command(["sudo", "apt-get", "install", "-y", "tor"], "Failed to install Tor", retries=2)

    print("[*] Starting Tor service...")
    run_command(["sudo", "service", "tor", "start"], "Failed to start Tor", retries=2)

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

# === DOWNLOAD THUMBNAIL ONLY ===
def download_thumbnail(link, out_dir):
    print("[*] Downloading video thumbnail only...")
    run_command([
        "yt-dlp",
        "--proxy", "socks5://127.0.0.1:9050",
        "--skip-download",
        "--write-thumbnail",
        "-o", os.path.join(out_dir, "thumb.%(ext)s"),
        link
    ], "Thumbnail download failed", retries=3, delay=7)

    # Rename downloaded thumbnail to thumbnail.jpeg/png
    thumb_files = glob.glob(os.path.join(out_dir, "thumb.*"))
    if not thumb_files:
        print("[✘] No thumbnail was downloaded.")
        sys.exit(1)

    original = thumb_files[0]
    ext = os.path.splitext(original)[1].lower()  # e.g., .jpg or .webp or .png
    new_name = os.path.join(out_dir, f"thumbnail{ext}")
    os.rename(original, new_name)
    print(f"[✓] Thumbnail saved as {new_name}")

# === MAIN FLOW ===
if __name__ == "__main__":
    link_file = "Vid/yt_link"
    output_dir = "Vid"

    os.makedirs(output_dir, exist_ok=True)

    start_tor()
    yt_url = read_youtube_link(link_file)
    print(f"[*] Downloading thumbnail from: {yt_url}")

    download_thumbnail(yt_url, output_dir)

    print("[✓] Thumbnail download complete.")
