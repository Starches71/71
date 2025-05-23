import subprocess
import os

# === SETUP TOR ===
def start_tor():
    subprocess.run(["sudo", "apt-get", "update"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "tor"], check=True)
    subprocess.run(["sudo", "service", "tor", "start"], check=True)

# === READ LINK ===
def read_youtube_link(file_path):
    with open(file_path, "r") as f:
        return f.read().strip()

# === DOWNLOAD VIDEO ONLY ===
def download_video_only(link, out_dir):
    try:
        print("Downloading video only...")
        subprocess.run([
            "yt-dlp",
            "--proxy", "socks5://127.0.0.1:9050",
            "-f", "bestvideo",
            "-o", os.path.join(out_dir, "avideo.%(ext)s"),
            link
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Video download failed: {e}")

# === DOWNLOAD AUDIO ONLY ===
def download_audio_only(link, out_dir):
    try:
        print("Downloading audio only...")
        subprocess.run([
            "yt-dlp",
            "--proxy", "socks5://127.0.0.1:9050",
            "-f", "bestaudio",
            "-o", os.path.join(out_dir, "audio.%(ext)s"),
            link
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Audio download failed: {e}")

# === DOWNLOAD THUMBNAIL ONLY ===
def download_thumbnail(link, out_dir):
    try:
        print("Downloading thumbnail...")
        subprocess.run([
            "yt-dlp",
            "--proxy", "socks5://127.0.0.1:9050",
            "--write-thumbnail",
            "--convert-thumbnails", "jpg",
            "-o", os.path.join(out_dir, "thumb.%(ext)s"),
            link
        ], check=True)

        # Rename the thumbnail
        for fname in os.listdir(out_dir):
            if fname.endswith(".jpg") and "thumb" in fname:
                os.rename(os.path.join(out_dir, fname), os.path.join(out_dir, "thumbnail.jpg"))
                break
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Thumbnail download failed: {e}")

# === MAIN FLOW ===
if __name__ == "__main__":
    link_file = "Vid/yt_link"
    output_dir = "Vid"

    start_tor()
    yt_url = read_youtube_link(link_file)
    print(f"Downloading from: {yt_url}")

    download_video_only(yt_url, output_dir)
    download_audio_only(yt_url, output_dir)
    download_thumbnail(yt_url, output_dir)

    print("All downloads complete.")
