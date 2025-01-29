
import subprocess

SEARCH_TERM = "Hilton Hotel"
VIDEO_PATH = "videos/video1.mp4"

# yt-dlp command with extractor args
command_extractor_args = [
    "yt-dlp", f"ytsearch3:{SEARCH_TERM}",
    "-o", "videos/video%(search_index)s.mp4",
    "--format", "best",
    "--extractor-args", "youtube:player_client=android"
]

# yt-dlp command with spoofed headers
command_spoof_headers = [
    "yt-dlp", f"ytsearch3:{SEARCH_TERM}",
    "-o", "videos/video%(search_index)s.mp4",
    "--format", "best",
    "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "--referer", "https://www.youtube.com/"
]

def run_command(command, method_name):
    try:
        print(f"\n🔍 Testing {method_name}...")
        result = subprocess.run(command, capture_output=True, text=True)
        
        if "ERROR" in result.stderr:
            print(f"❌ {method_name} failed!\n{result.stderr}")
            return False
        else:
            print(f"✅ {method_name} succeeded!")
            return True
    except Exception as e:
        print(f"❌ {method_name} encountered an error: {str(e)}")
        return False

# Run both methods
extractor_args_success = run_command(command_extractor_args, "Extractor Args")
spoof_headers_success = run_command(command_spoof_headers, "Spoofed Headers")

# Check if any videos were downloaded
import os
downloaded_files = os.listdir("videos") if os.path.exists("videos") else []

if downloaded_files:
    print("\n🎉 Some videos were successfully downloaded!")
else:
    print("\n❌ No videos were downloaded. Both methods failed.")
