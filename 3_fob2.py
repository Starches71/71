
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

# === TOR SETUP ===
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

# === READERS ===
def read_filter_result(path="Vid/filter_result.txt"):
    try:
        with open(path, "r") as f:
            result = f.read().strip().lower()
            return result == "no"
    except Exception as e:
        print(f"[ERROR] Could not read filter result: {e}")
        sys.exit(1)

def read_youtube_link(path="Vid/yt_link"):
    try:
        with open(path, "r") as f:
            link = f.read().strip()
            if not link:
                raise ValueError("YouTube link file is empty.")
            return link
    except Exception as e:
        print(f"[ERROR] Could not read YouTube link: {e}")
        sys.exit(1)

# === DOWNLOAD VIDEO ===
def download_full_video(link, out_dir):
    print("[*] Downloading video via yt-dlp + Tor...")
    run_command([
        "yt-dlp",
        "--proxy", "socks5://127.0.0.1:9050",
        "--merge-output-format", "mp4",
        "-o", os.path.join(out_dir, "VIDEO.%(ext)s"),
        link
    ], "Video download failed", retries=3, delay=7)

# === MAIN FLOW ===
if __name__ == "__main__":
    output_dir = "Vid"
    os.makedirs(output_dir, exist_ok=True)

    if not read_filter_result():
        print("[✘] Video flagged by filter (haram, music, face, etc). Skipping download.")
        sys.exit(0)

    start_tor()
    yt_url = read_youtube_link()
    print(f"[*] Clean video detected. Downloading from: {yt_url}")

    download_full_video(yt_url, output_dir)
    print("[✓] Video download complete. Saved to 'Vid/VIDEO.mp4' (or other extension)")
