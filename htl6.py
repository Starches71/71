import os
import subprocess

# Paths
descriptions_dir = "best_descriptions"
places_dir = "places"
links_dir = "best_link"

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

# Process each hotel file in the descriptions directory
for hotel_file in hotel_files:
    try:
        # Extract the hotel name by removing the number and file extension
        hotel_name = hotel_file.split('.')[1].strip()
        print(f"Processing hotel: {hotel_name}")

        # Construct the search query
        search_query = f"{hotel_name} {place_name}"
        print(f"Search query: {search_query}")

        # Ensure Tor is running (this is to ensure it is activated before using torsocks)
        subprocess.run(["tor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # yt-dlp command to search for 3 video links related to the hotel and place
        command = [
            'torsocks', 'yt-dlp', f"ytsearch3:{search_query}",  # Use torsocks with yt-dlp
            '--print', 'id',  # Print only video IDs
            '--skip-download'  # Skip downloading videos
        ]
        print(f"Running command: {' '.join(command)}")

        # Run the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True)

        # Check for errors in yt-dlp execution
        if result.returncode != 0:
            print(f"Error fetching videos for {hotel_name}: {result.stderr.strip()}")
            continue

        # Process video IDs to construct YouTube URLs
        video_ids = result.stdout.strip().split('\n')
        video_urls = [f"https://youtu.be/{video_id}" for video_id in video_ids if video_id.strip()]

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
