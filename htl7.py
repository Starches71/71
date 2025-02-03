
import os
import subprocess
import time
import requests
import traceback

# Directory paths
links_dir = "best_link"
output_dir = "best_vid"
cookies_file = "cookies.txt"  # Path to the cookies.txt file
api_key = "00181c98c6mshb28efee02d1aa4cp101a3bjsn810e9f1a5717"  # Your RapidAPI key
rapidapi_host = "youtube-search.p.rapidapi.com"

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to fetch video download URL using RapidAPI
def fetch_video_download_link(search_query):
    url = "https://youtube-search.p.rapidapi.com/search"
    querystring = {"key": "AIzaSyAOsteuaW5ifVvA_RkLXh0mYs6GLAD6ykc", "part": "snippet", "q": search_query}
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

    # Check if there are any results
    if "items" in video_data:
        video_id = video_data["items"][0]["id"]["videoId"]  # Get the first video ID
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return video_url
    else:
        print("No videos found for query:", search_query)
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
                download_link = fetch_video_download_link(link)

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
