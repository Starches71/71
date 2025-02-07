
import os
import requests
import time

# RapidAPI details for YouTube Downloader
API_URL = "https://youtube-downloader-videos.p.rapidapi.com/"  # RapidAPI URL
API_KEY = "00181c98c6mshb28efee02d1aa4cp101a3bjsn810e9f1a5717"  # Your RapidAPI key
QUALITY = "720"  # Video quality (you can adjust this as needed)

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

        # For each link, request video download from RapidAPI
        for idx, link in enumerate(links):
            link = link.strip()
            if not link:
                continue  # Skip empty lines

            # Construct output filename
            suffix = chr(65 + idx)  # Converts 0 to 'A', 1 to 'B', etc.
            output_filename = f"{links_file.split('.')[0]}{suffix}.mp4"
            output_filepath = os.path.join(output_dir, output_filename)

            # Prepare query parameters and headers for the API request
            querystring = {"url": link, "quality": QUALITY}
            headers = {
                "x-rapidapi-key": API_KEY,
                "x-rapidapi-host": "youtube-downloader-videos.p.rapidapi.com"
            }

            # Attempt download (retry once on failure)
            for attempt in range(2):
                try:
                    response = requests.get(API_URL, headers=headers, params=querystring)

                    if response.status_code == 200:
                        data = response.json()
                        download_url = data.get('download_url')  # Assuming the API returns a download URL
                        if download_url:
                            # Start downloading the video file
                            video_response = requests.get(download_url)
                            with open(output_filepath, 'wb') as f:
                                f.write(video_response.content)
                            print(f"Download started for {link} ({output_filename})")
                            break  # Exit retry loop on success
                        else:
                            print(f"Error: No download URL returned for {link}")
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
