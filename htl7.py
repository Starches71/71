
import os
import subprocess
import time

# Directory paths
links_dir = "best_link"
output_dir = "best_vid"

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to start Tor
def start_tor():
    print("Starting Tor service...")
    tor_process = subprocess.Popen(["tor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(10)  # Give Tor enough time to initialize
    return tor_process

# Function to stop Tor
def stop_tor(process):
    if process:
        print("Stopping Tor service...")
        process.terminate()
        process.wait()

# Start Tor initially
tor_process = start_tor()

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
            output_path = os.path.join(output_dir, output_filename)

            # Retry mechanism if an error occurs
            max_retries = 3
            retry_count = 0

            while retry_count < max_retries:
                # yt-dlp command to download the segment using torsocks
                command = [
                    'torsocks', 'yt-dlp', '-o', output_path,
                    '--download-sections', '*00:10-01:00',
                    link
                ]

                print(f"Downloading {link} (Attempt {retry_count + 1}/{max_retries})...")

                # Run the command
                result = subprocess.run(command, capture_output=True, text=True)

                # Check if the download was successful
                if result.returncode == 0 and os.path.exists(output_path):
                    print(f"Downloaded {output_filename} successfully!")
                    break  # Exit retry loop on success
                else:
                    print(f"Error downloading {link}: {result.stderr.strip()}")
                    retry_count += 1

                    if retry_count < max_retries:
                        print(f"Retrying with a new Tor circuit... (Attempt {retry_count + 1}/{max_retries})")
                        stop_tor(tor_process)  # Stop current Tor instance
                        tor_process = start_tor()  # Start new Tor instance
                    else:
                        print(f"Max retries reached for {link}. Skipping...")

# Stop Tor after execution
stop_tor(tor_process)
