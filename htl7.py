
import os
import subprocess
import time

# Directory paths
links_dir = "best_link"
output_dir = "best_vid"

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# **Start Tor Service**
print("Starting Tor service...")
tor_process = subprocess.Popen(["tor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(5)  # Wait for Tor to initialize

# Iterate through each .links.txt file in the links directory
for links_file in os.listdir(links_dir):
    if links_file.endswith('.links.txt'):
        file_path = os.path.join(links_dir, links_file)

        # Read all links from the current file
        with open(file_path, 'r') as f:
            links = f.readlines()

        # For each link, download a 45-second segment starting from 10 seconds
        for idx, link in enumerate(links):
            link = link.strip()

            # Construct the output file name with suffixes like A, B, C
            suffix = chr(65 + idx)  # Converts 0 to 'A', 1 to 'B', etc.
            output_filename = f"{links_file.split('.')[0]}{suffix}.mp4"

            # yt-dlp command to download the segment using torsocks
            command = [
                'torsocks', 'yt-dlp', '-o', os.path.join(output_dir, output_filename),
                '--download-sections', '*00:10-01:00',
                link
            ]

            # Run the command
            subprocess.run(command)

            print(f"Downloaded segment for {link} and saved as {output_filename}")

# **Stop Tor process after execution**
print("Stopping Tor service...")
tor_process.terminate()
tor_process.wait()
