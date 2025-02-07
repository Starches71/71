import os
import requests
import time

# API details
API_URL = "http://127.0.0.1:5000/download/best"  # Automatically selects the best format

# Directory paths
links_dir = "best_link"
output_dir = "best_vid"

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterate through each .links.txt file in the links directory
for links_file in os.listdir(links_dir):
    if links_file.endswith('.links.txt'):
        file_path = os.path.join(links_dir, links_file)

        # Read all links from the current file
        with open(file_path, 'r') as f:
            links = f.readlines()

        # For each link, request video download
        for idx, link in enumerate(links):
            link = link.strip()
            if not link:
                continue  # Skip empty lines

            # Construct output filename
            suffix = chr(65 + idx)  # Converts 0 to 'A', 1 to 'B', etc.
            output_filename = f"{links_file.split('.')[0]}{suffix}.mp4"

            # Attempt download (retry once on failure)
            for attempt in range(2):
                try:
                    response = requests.post(API_URL, json={"url": link})

                    if response.status_code == 200:
                        print(f"Download started for {link} ({output_filename})")
                        break  # Exit retry loop on success
                    else:
                        print(f"Error downloading {link}: {response.json()}")
                        if attempt == 0:
                            print("Retrying...")
                            time.sleep(3)  # Wait before retrying
                except requests.RequestException as e:
                    print(f"Network error for {link}: {e}")
                    if attempt == 0:
                        print("Retrying...")
                        time.sleep(3)  # Wait before retrying

            # Delay to prevent overloading API
            time.sleep(2)
