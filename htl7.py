
import os
import subprocess
import time
import requests
import traceback

# Directory paths
links_dir = "best_link"
output_dir = "best_vid"
cookies_file = "cookies.txt"  # Path to the cookies.txt file
api_key = "cfb23850e4msh938d8d31212b669p180be8jsnfb2af52d947e"  # Your new RapidAPI key
rapidapi_host = "youtube-info-download-api.p.rapidapi.com"

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to fetch video download URL using RapidAPI
def fetch_video_download_link(video_id):
    url = "https://youtube-info-download-api.p.rapidapi.com/ajax/progress.php"
    querystring = {"id": video_id}
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": rapidapi_host
    }

    # Send the request to the API
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        print(f"Error: Unable to fetch data from API. Status code: {response.status_code}")
        return None

    # Parse the response JSON
    video_data = response.json()

    # Check if the response contains download links
    if "video" in video_data and "downloads" in video_data["video"]:
        download_links = video_data["video"]["downloads"]
        # We can choose the best available quality for download (e.g., highest quality)
        for download in download_links:
            if download.get("quality") == "1080p":  # Choose 1080p or any quality you prefer
                return download.get("url")
    else:
        print(f"No download links found for video ID: {video_id}")
        return None

# Iterate through each .links.txt file in the links directory
for links_file in os.listdir(links_dir):
    if links_file.endswith('.links.txt'):
        file_path = os.path.join(links_dir, links_file)

        # Read all links from the current file
        with open(file_path, 'r') as f:
            links = f.readlines()

        # For each link, download the video using RapidAPI
        for idx, link in enumerate(links):
            link = link.strip()
            if not link:
                continue

            # Extract the video ID from the link (YouTube video ID is in the URL)
            video_id = link.split("v=")[-1]  # Extract video ID from YouTube URL
            if "&" in video_id:
                video_id = video_id.split("&")[0]  # In case there are additional parameters

            # Construct the output file name with suffixes like A, B, C
            filename_base, _ = os.path.splitext(links_file)  # Better filename handling
            suffix = chr(65 + idx)  # Converts 0 to 'A', 1 to 'B', etc.
            output_filename = f"{filename_base}{suffix}.mp4"
            output_path = os.path.join(output_dir, output_filename)

            # Retry mechanism if an error occurs
            max_retries = 3
            retry_count = 0

            while retry_count < max_retries:
                # Fetch video download link using RapidAPI
                download_link = fetch_video_download_link(video_id)

                if download_link:
                    # Use curl to download the video
                    command = ['curl', '-L', '-o', output_path, download_link]

                    print(f"Downloading {download_link} to {output_filename} (Attempt {retry_count + 1}/{max_retries})...")

                    try:
                        result = subprocess.run(command, capture_output=True, text=True)

                        # Check if the download was successful
                        if result.returncode == 0 and os.path.exists(output_path):
                            print(f"Downloaded {output_filename} successfully!")
                            break  # Exit retry loop on success
                        else:
                            print(f"Error downloading {download_link}: {result.stderr.strip()}")
                            retry_count += 1

                            if retry_count < max_retries:
                                print(f"Retrying in 10 seconds... (Attempt {retry_count + 1}/{max_retries})")
                                time.sleep(10)  # Wait before retrying
                            else:
                                print(f"Max retries reached for {download_link}. Skipping...")
                    except Exception as e:
                        print(f"An error occurred while downloading {download_link}: {e}")
                        print("Detailed error traceback:")
                        traceback.print_exc()
                else:
                    print(f"Failed to retrieve a download link for {link}")
                    break  # Skip to the next link if no download link was found
