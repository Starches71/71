
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
    time.sleep(15)  # Give Tor more time to initialize
    return tor_process

# Function to stop Tor
def stop_tor(process):
    if process:
        print("Stopping Tor service...")
        process.terminate()
        process.wait()

# Function to verify Tor connection
def verify_tor_connection():
    print("Verifying Tor connection...")
    # Run curl with torsocks to check if the connection goes through Tor
    command = ["torsocks", "curl", "https://check.torproject.org"]
    result = subprocess.run(command, capture_output=True, text=True)

    # Check if the connection was successful
    if "Congratulations" in result.stdout:
        print("Tor is successfully routed through the network!")
        return True
    else:
        print("Failed to verify Tor connection.")
        return False

# Start Tor initially
tor_process = start_tor()

# Verify the Tor connection before proceeding
if not verify_tor_connection():
    print("Exiting due to failed Tor connection verification.")
    stop_tor(tor_process)
    exit()

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
            if not link:
                continue

            # Construct the output file name with suffixes like A, B, C
            filename_base, _ = os.path.splitext(links_file)  # Better filename handling
            suffix = chr(65 + idx)  # Converts 0 to 'A', 1 to 'B', etc.
            output_filename = f"{filename_base}{suffix}.mp4"
            output_path = os.path.join(output_dir, output_filename)

            # Retry mechanism if an error occurs
            max_retries = 3
            retry_count = 0

            while retry_count < max_retries:
                # yt-dlp command to download the segment using torsocks, with verbosity
                command = [
                    'torsocks', 'yt-dlp', '-v',  # -v for verbose output
                    '-o', output_path,
                    '--download-sections', "*10-55",  # Download segment from 10-55 seconds
                    link
                ]

                print(f"Downloading {link} (Attempt {retry_count + 1}/{max_retries})...")

                # Run the command and capture the output
                result = subprocess.run(command, capture_output=True, text=True)

                # Check if the download was successful
                if result.returncode == 0 and os.path.exists(output_path):
                    print(f"Downloaded {output_filename} successfully!")
                    break  # Exit retry loop on success
                else:
                    print(f"Error downloading {link}: {result.stderr.strip()}")
                    print(f"stdout: {result.stdout.strip()}")  # Output from the command
                    retry_count += 1

                    if retry_count < max_retries:
                        print(f"Retrying in 10 seconds... (Attempt {retry_count + 1}/{max_retries})")
                        time.sleep(10)  # Wait before retrying
                    else:
                        print(f"Max retries reached for {link}. Skipping...")

# Stop Tor after execution
stop_tor(tor_process)
