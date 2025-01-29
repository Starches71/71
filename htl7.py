import os
import subprocess

# Directory paths
links_dir = "best_link"
output_dir = "best_vid"

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"📁 Created output directory: {output_dir}")

# Get all .links.txt files
links_files = [f for f in os.listdir(links_dir) if f.endswith('.links.txt')]
if not links_files:
    print(f"🚨 No '.links.txt' files found in {links_dir}")
    exit(1)

# Process each .links.txt file
for links_file in links_files:
    file_path = os.path.join(links_dir, links_file)
    print(f"\n📂 Processing file: {links_file}")

    try:
        with open(file_path, 'r') as f:
            links = f.readlines()
        print(f"🔗 Found {len(links)} links in {links_file}")
    except Exception as e:
        print(f"❌ Error reading {links_file}: {e}")
        continue

    # Download each video segment
    for idx, link in enumerate(links):
        link = link.strip()
        if not link:
            print(f"⚠️ Skipping empty link at index {idx} in {links_file}")
            continue

        suffix = chr(65 + idx)  # 'A', 'B', 'C', etc.
        output_filename = f"{links_file.split('.')[0]}{suffix}.mp4"
        output_path = os.path.join(output_dir, output_filename)

        print(f"🎬 Downloading: {link} -> {output_filename}")

        # First, get the video duration
        duration_command = ["yt-dlp", "--get-duration", link]
        duration_result = subprocess.run(duration_command, capture_output=True, text=True)
        duration_str = duration_result.stdout.strip()

        if duration_result.returncode != 0 or not duration_str:
            print(f"❌ Error getting duration for {link}: {duration_result.stderr.strip()}")
            continue

        # Convert duration to seconds
        time_parts = list(map(int, duration_str.split(":")))
        if len(time_parts) == 3:
            duration_sec = time_parts[0] * 3600 + time_parts[1] * 60 + time_parts[2]
        elif len(time_parts) == 2:
            duration_sec = time_parts[0] * 60 + time_parts[1]
        else:
            duration_sec = time_parts[0]

        # Decide download method based on video length
        if duration_sec >= 60:
            download_sections = "*00:10-01:00"
        else:
            download_sections = "*"  # Download full video

        # Use yt-dlp with torsocks
        command = [
            "torsocks", "yt-dlp",
            "-o", output_path,
            "--download-sections", download_sections,
            "--no-part", "--verbose",
            link
        ]

        result = subprocess.run(command, capture_output=True, text=True)

        # DEBUG: Print yt-dlp output for troubleshooting
        print(f"🔍 yt-dlp output: {result.stdout.strip()}")
        print(f"⚠️ yt-dlp errors: {result.stderr.strip()}")

        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"✅ Successfully downloaded and saved: {output_path}")
        else:
            print(f"❌ Download failed: {output_path}")
            print(f"🔎 yt-dlp might have encountered an issue.")

# Final check: list all downloaded files
print("\n📂 Final check: Listing files in best_vid/")
saved_files = os.listdir(output_dir)
if saved_files:
    print("\n".join(saved_files))
else:
    print("🚨 No files found in best_vid!")
