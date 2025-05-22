
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

# === DOWNLOAD VIDEO & THUMBNAIL ===
def download_video_and_thumbnail(link, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    
    # Download video
    subprocess.run([
        "yt-dlp",
        "--proxy", "socks5://127.0.0.1:9050",
        "-f", "bestvideo+bestaudio",
        "-o", os.path.join(out_dir, "Video.%(ext)s"),
        "--write-thumbnail",
        "--convert-thumbnails", "jpg",
        "--output", os.path.join(out_dir, "Video.%(ext)s"),
        link
    ], check=True)
    
    # Rename thumbnail if it exists
    for fname in os.listdir(out_dir):
        if fname.endswith(".jpg") and "Video" in fname and "thumb" in fname:
            os.rename(os.path.join(out_dir, fname), os.path.join(out_dir, "thumbnail.jpg"))
            break

# === MAIN FLOW ===
if __name__ == "__main__":
    link_file = "Vid/yt_link"
    output_dir = "Vid"
    
    start_tor()
    yt_url = read_youtube_link(link_file)
    print(f"Downloading from: {yt_url}")
    download_video_and_thumbnail(yt_url, output_dir)
    print("Done.")
