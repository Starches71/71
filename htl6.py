import os
import requests
import traceback

# Paths
descriptions_dir = "best_descriptions"
places_dir = "places"
links_dir = "best_link"

# Your YouTube API Key
YOUTUBE_API_KEY = "AIzaSyCOv3Fv5dPw9yDPKyssYo-Yz36HSJQdlqI"

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

# Function to fetch video links using YouTube API
def fetch_video_links(search_query, max_results=3):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={search_query}&type=video&maxResults={max_results}&key={YOUTUBE_API_KEY}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error fetching video links: {response.text}")
        return None

    data = response.json()
    video_ids = [item["id"]["videoId"] for item in data.get("items", []) if "id" in item and "videoId" in item["id"]]
    
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
            # Fetch video links using YouTube API
            video_ids = fetch_video_links(search_query)

            if video_ids:  # Check if we fetched video IDs successfully
                break  # Success, exit retry loop
            else:
                retry_count += 1
                if retry_count < max_retries:
                    print(f"Retrying... (Attempt {retry_count + 1}/{max_retries})")
                else:
                    print(f"Max retries reached for {hotel_name}. Skipping...")
                    continue  # Skip to the next hotel

        if not video_ids:  # If no video IDs were found, continue to the next hotel
            print(f"No video IDs found for {hotel_name}")
            continue

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
        print("Detailed error traceback:")
        traceback.print_exc()
