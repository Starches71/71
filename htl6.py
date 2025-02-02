import os
import subprocess
import time
import requests

# Paths
descriptions_dir = "best_descriptions"
places_dir = "places"
links_dir = "best_link"
cookies_file = "cookies.txt"  # Define cookies.txt location

# Create the links directory if it doesn't exist
if not os.path.exists(links_dir):
    os.makedirs(links_dir)
    print(f"Created directory: {links_dir}")
else:
    print(f"Directory already exists: {links_dir}")

# Read the place name from the first line of the places file
try:
    with open(os.path.join(places_dir, "places.txt"), "r") as f:
        place_name = f.readline().strip()
    print(f"Place name extracted: {place_name}")
except Exception as e:
    print(f"Error reading 'places.txt': {e}")
    exit(1)

# List hotel description files
hotel_files = os.listdir(descriptions_dir)
if not hotel_files:
    print(f"No files found in directory: {descriptions_dir}")
    exit(1)
else:
    print(f"Found {len(hotel_files)} files in '{descriptions_dir}'")

# Function to fetch video links using curl
def fetch_video_links_via_curl(search_query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Construct the search URL (YouTube search)
    search_url = f"https://www.youtube.com/results?search_query={search_query}"

    # Use curl with cookies and headers
    curl_command = [
        'curl', '-s',  # Use curl without torsocks
        '-b', cookies_file,  # Use cookies from cookies.txt
        '-A', headers['User-Agent'],  # Set the User-Agent header
        search_url
    ]

    # Run curl command
    result = subprocess.run(curl_command, capture_output=True, text=True)

    # Check if the command was successful
    if result.returncode != 0:
        print(f"Error fetching links: {result.stderr}")
        return None

    # Extract video IDs from the HTML response using a regex pattern
    import re
    video_ids = re.findall(r'/"videoId":"([^"]+)"', result.stdout)
    return video_ids

# Process each hotel file in the descriptions directory
for hotel_file in hotel_files:
    try:
        # Extract the hotel name by removing the number and file extension
        hotel_name = hotel_file.split('.')[1].strip()
        print(f"Processing hotel: {hotel_name}")

        # Construct the search query
        search_query = f"{hotel_name} {place_name}"
        print(f"Search query: {search_query}")

        # Retry mechanism if an error occurs
        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            # Fetch video links using curl with cookies
            video_ids = fetch_video_links_via_curl(search_query)

            if video_ids:  # Check if we fetched video IDs successfully
                break  # Success, exit retry loop
            else:
                retry_count += 1
                if retry_count < max_retries:
                    print(f"Retrying... (Attempt {retry_count + 1}/{max_retries})")
                else:
                    print(f"Max retries reached for {hotel_name}. Skipping...")
                    continue  # Skip to the next hotel

        # Construct YouTube URLs
        video_urls = [f"https://youtu.be/{video_id}" for video_id in video_ids]

        if not video_urls:
            print(f"No video URLs found for {hotel_name}")
            continue

        # Save the video URLs to a file in the 'best_link' directory
        links_file_path = os.path.join(links_dir, f"{hotel_file.split('.')[0]}.links.txt")
        with open(links_file_path, "w") as links_file:
            for url in video_urls:
                links_file.write(url + '\n')
        print(f"Fetched URLs for {hotel_name} and saved to {links_file_path}")

    except Exception as e:
        print(f"An error occurred while processing {hotel_file}: {e}")
