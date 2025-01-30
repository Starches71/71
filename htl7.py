
import os
from pytube import YouTube

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

        try:
            # Create a YouTube object
            yt = YouTube(link)

            # Choose the stream with the highest resolution and progressive download (audio+video)
            stream = yt.streams.filter(progressive=True, file_extension="mp4").get_highest_resolution()

            # Download the video to the output path
            stream.download(output_path=output_dir, filename=output_filename)

            # Check if download was successful
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"✅ Successfully downloaded and saved: {output_path}")
            else:
                print(f"❌ Download failed: {output_path}")
        except Exception as e:
            print(f"❌ Error downloading {link}: {e}")

# Final check: list all downloaded files
print("\n📂 Final check: Listing files in best_vid/")
saved_files = os.listdir(output_dir)
if saved_files:
    print("\n".join(saved_files))
else:
    print("🚨 No files found in best_vid!")
