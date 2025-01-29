
import os
import subprocess

# Install yt-dlp-5 if not installed
try:
    import yt_dlp
except ImportError:
    print("Installing yt-dlp-5...")
    subprocess.run(["pip", "install", "-U", "git+https://github.com/yt-dlp/yt-dlp.git@yt-dlp-5"], check=True)

# Output directory
output_dir = "videos"
os.makedirs(output_dir, exist_ok=True)

# Search term
search_term = "Hilton Hotel"

# yt-dlp-5 command to search and download 3 videos
command = [
    "yt-dlp", 
    f"ytsearch3:{search_term}",  # Search for 3 videos
    "-o", os.path.join(output_dir, "video%(search_index)s.mp4"),  # Save as video1.mp4, video2.mp4, etc.
    "--format", "best",  # Best available format
    "--no-warnings", "--quiet",  # Reduce logs
    "--no-part"  # Prevents temporary files
]

print(f"Running command: {' '.join(command)}")

# Run yt-dlp-5
result = subprocess.run(command, capture_output=True, text=True)

# Print stdout and stderr
print("\n✅ STDOUT:")
print(result.stdout.strip())

print("\n❌ STDERR:")
print(result.stderr.strip())

# Check if videos were downloaded successfully
print("\n📂 Checking downloaded videos...")
for i in range(1, 4):
    video_path = os.path.join(output_dir, f"video{i}.mp4")
    if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
        print(f"✅ Success: {video_path}")
    else:
        print(f"❌ Failed: {video_path} not found or empty")
