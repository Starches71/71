
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

        # Force a new Tor identity before each download (optional)
        subprocess.run(["torsocks", "curl", "--silent", "https://check.torproject.org/"])

        # Use yt-dlp with torsocks
        command = ["torsocks", "yt-dlp", "-o", output_path, "--download-sections", "*00:10-01:00", link]

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            if os.path.exists(output_path):
                print(f"✅ Successfully downloaded and saved: {output_path}")
            else:
                print(f"❌ Downloaded but file is missing: {output_path}")
        else:
            print(f"❌ Error downloading {link}: {result.stderr.strip()}")

# Final check: list all downloaded files
print("\n📂 Final check: Listing files in best_vid/")
saved_files = os.listdir(output_dir)
if saved_files:
    print("\n".join(saved_files))
else:
    print("🚨 No files found in best_vid!")
