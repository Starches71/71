
import os
import subprocess

# Directory paths
links_dir = "best_link"
output_dir = "best_vid"

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created output directory: {output_dir}")
else:
    print(f"Output directory already exists: {output_dir}")

# Check if there are any .links.txt files in the links directory
links_files = [f for f in os.listdir(links_dir) if f.endswith('.links.txt')]
if not links_files:
    print(f"No '.links.txt' files found in directory: {links_dir}")
    exit(1)
else:
    print(f"Found {len(links_files)} '.links.txt' files in '{links_dir}'")

# Iterate through each .links.txt file in the links directory
for links_file in links_files:
    file_path = os.path.join(links_dir, links_file)
    print(f"\nProcessing file: {links_file}")

    # Read all links from the current file
    try:
        with open(file_path, 'r') as f:
            links = f.readlines()
        print(f"Found {len(links)} links in {links_file}")
    except Exception as e:
        print(f"Error reading file {links_file}: {e}")
        continue

    # For each link, download a 45-second segment starting from 10 seconds
    for idx, link in enumerate(links):
        link = link.strip()
        if not link:
            print(f"Skipping empty link at index {idx} in {links_file}")
            continue

        # Construct the output file name with suffixes like A, B, C
        try:
            suffix = chr(65 + idx)  # Converts 0 to 'A', 1 to 'B', etc.
            output_filename = f"{links_file.split('.')[0]}{suffix}.mp4"
            output_path = os.path.join(output_dir, output_filename)
            print(f"Downloading segment from {link} to {output_filename}")

            # Define the section to download: *00:10-01:00 (45 seconds)
            command = [
                'torsocks', 'yt-dlp', '-o', output_path,
                '--download-sections', '*00:10-01:00', link
            ]

            # Run the command and capture output
            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"Successfully downloaded segment for {link} and saved as {output_filename}")
            else:
                print(f"Error downloading from {link}: {result.stderr.strip()}")

        except Exception as e:
            print(f"An error occurred while processing link {link}: {e}")

# After completing the download, run htl8.py
try:
    print("\nRunning htl8.py...")
    subprocess.run(["python", "htl8.py"], check=True)
    print("htl8.py executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error running htl8.py: {e}")
