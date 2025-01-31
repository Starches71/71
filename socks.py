
import subprocess
import os

# Function to activate Tor and run yt-dlp using torsocks
def run_torsocks_yt_dlp():
    try:
        # Step 1: Start Tor service
        print("Starting Tor...")
        subprocess.run(["tor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Tor started successfully!")

        # Step 2: Search for the first video using yt-dlp with torsocks
        search_term = "Sherston jeddah hotel"
        print(f"Searching for video: {search_term}")
        
        # Run yt-dlp with torsocks to search for videos
        command = [
            "torsocks", "yt-dlp", f"ytsearch1:{search_term}",
            "--print", "id",  # Print only video ID
            "--skip-download"  # Don't download the video yet, just get the video ID
        ]
        result = subprocess.run(command, capture_output=True, text=True)

        # Check for errors
        if result.returncode != 0:
            print(f"Error searching video: {result.stderr.strip()}")
            return
        
        # Extract video ID from the output
        video_id = result.stdout.strip()
        if not video_id:
            print(f"No video found for the search term '{search_term}'")
            return
        
        print(f"Found video ID: {video_id}")

        # Step 3: Download the first video using yt-dlp with torsocks
        video_url = f"https://youtu.be/{video_id}"
        print(f"Downloading video: {video_url}")

        # Define output file path
        output_dir = "downloaded_videos"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_filename = os.path.join(output_dir, f"{video_id}.mp4")

        # Run yt-dlp to download the video
        command = [
            "torsocks", "yt-dlp", "-o", output_filename, video_url
        ]
        subprocess.run(command)
        print(f"Downloaded video and saved as: {output_filename}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function
if __name__ == "__main__":
    run_torsocks_yt_dlp()
