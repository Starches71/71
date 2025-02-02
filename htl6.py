
import os
import subprocess
import time

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

# Function to monitor torsocks usage and try different configurations
def run_torsocks_with_verbosity(command):
    print(f"Running command with torsocks: {' '.join(command)}")
    # Run the command using torsocks and capture output
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Print verbose logs for debugging
    print("Command output (stdout):", result.stdout)
    print("Command error (stderr):", result.stderr)
    
    if result.returncode != 0:
        print(f"Error with torsocks: {result.stderr.strip()}")
        return None  # Return None to indicate failure
    
    return result.stdout  # Return successful output

# Start Tor initially
tor_process = start_tor()

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
            # yt-dlp command to search for 3 video links related to the hotel and place
            command = [
                'torsocks', 'yt-dlp', f"ytsearch3:{search_query}",  # Use torsocks with yt-dlp
                '--print', 'id',  # Print only video IDs
                '--skip-download',  # Skip downloading videos
                '-v'  # Add verbosity flag to yt-dlp
            ]

            # Run the command and capture the output using the defined function
            result_output = run_torsocks_with_verbosity(command)

            if result_output is not None:  # Check if the command was successful
                break  # Success, exit retry loop
            else:
                retry_count += 1
                if retry_count < max_retries:
                    print(f"Retrying with new Tor circuit... (Attempt {retry_count + 1}/{max_retries})")
                    stop_tor(tor_process)  # Stop current Tor instance
                    tor_process = start_tor()  # Start new Tor instance
                else:
                    print(f"Max retries reached for {hotel_name}. Skipping...")
                    continue  # Skip to the next hotel

        # Process video IDs to construct YouTube URLs
        video_ids = result_output.strip().split('\n') if result_output else []
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

# Stop Tor after execution
stop_tor(tor_process)
