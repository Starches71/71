
import os
import subprocess
import time

# Function to restart Tor
def restart_tor():
    print("🔄 Restarting Tor service...")
    subprocess.run(["sudo", "systemctl", "restart", "tor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(5)  # Wait for Tor to restart

# Function to check if torsocks is working
def test_torsocks():
    print("🛠️ Checking Tor connection...")
    test_cmd = ["torsocks", "curl", "--silent", "https://check.torproject.org/"]
    result = subprocess.run(test_cmd, capture_output=True, text=True)
    if "Congratulations" in result.stdout:
        print("✅ Tor is working!")
        return True
    else:
        print("❌ Tor is NOT working! Check your configuration.")
        return False

# Restart Tor and test connection
restart_tor()
if not test_torsocks():
    print("🚨 Exiting: Tor is not working.")
    exit(1)

# Directory paths
links_dir = "best_link"
output_dir = "best_vid"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"📁 Created output directory: {output_dir}")

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

        # yt-dlp command with torsocks
        command = [
            "torsocks", "yt-dlp", "-o", output_path,
            "--download-sections", "*00:10-01:00", link
        ]

        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Successfully downloaded: {output_filename}")
        else:
            print(f"❌ Error downloading {link}: {result.stderr.strip()}")
