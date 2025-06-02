
import subprocess
import os

# === SETUP TOR ===
def start_tor():
    try:
        print("[*] Updating package list...")
        subprocess.run(["sudo", "apt-get", "update"], check=True)

        print("[*] Installing Tor...")
        subprocess.run(["sudo", "apt-get", "install", "-y", "tor"], check=True)

        print("[*] Starting Tor service...")
        subprocess.run(["sudo", "service", "tor", "start"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to setup Tor: {e}")
        exit(1)

# === READ LINK ===
def read_youtube_link(file_path):
    try:
        with open(file_path, "r") as f:
            return f.read().strip()
    except Exception as e:
        print(f"[ERROR] Could not read YouTube link: {e}")
        exit(1)

# === DOWNLOAD FULL VIDEO (Video + Audio) ===
def download_full_video(link, out_dir):
    try:
        print("[*] Downloading full video with audio...")
        subprocess.run([
            "yt-dlp",
            "--proxy", "socks5://127.0.0.1:9050",
            "-f", "best",
            "-o", os.path.join(out_dir, "video.%(ext)s"),
            link
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Video download failed: {e}")
        exit(1)

# === MAIN FLOW ===
if __name__ == "__main__":
    link_file = "Vid/yt_link"
    output_dir = "Vid"

    # Make sure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    start_tor()
    yt_url = read_youtube_link(link_file)
    print(f"[*] Downloading from: {yt_url}")

    download_full_video(yt_url, output_dir)

    print("[✓] Download complete.")
