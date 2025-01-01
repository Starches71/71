import os
import requests
from yt_dlp import YoutubeDL

# Function to download video
def download_video(url, output_path, cookies_path=None):
    ydl_opts = {
        'outtmpl': output_path,
        'noplaylist': True,
        'format': 'bestvideo+bestaudio/best',
    }
    if cookies_path:
        ydl_opts['cookiefile'] = cookies_path

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Function to upload video via InnerTube API
def upload_video(file_path, title, description, cookies_path):
    # Read cookies from file
    with open(cookies_path, 'r') as f:
        cookies = f.read()

    # YouTube InnerTube upload endpoint
    upload_url = "https://www.youtube.com/upload_video"

    headers = {
        "Content-Type": "multipart/form-data",
        "Authorization": f"Bearer {cookies}",  # Use cookies for auth
    }

    # Payload for metadata
    metadata = {
        "title": title,
        "description": description,
    }

    # Upload video file
    with open(file_path, 'rb') as video_file:
        files = {
            "video": video_file,
            "metadata": (None, str(metadata)),
        }
        response = requests.post(upload_url, headers=headers, files=files)

    if response.status_code == 200:
        print("Video uploaded successfully!")
        print("Response:", response.json())
    else:
        print("Failed to upload video.")
        print("Response:", response.text)

# Main function
def main():
    video_url = "https://youtu.be/s7yBWncUrI0"  # Replace with your desired video URL
    output_path = "downloaded_video.mp4"
    cookies_path = "cookies.txt"

    # Step 1: Download video
    print("Downloading video...")
    download_video(video_url, output_path, cookies_path)

    # Step 2: Upload video
    print("Uploading video...")
    title = "Random 10-second video"
    description = "This is an auto-posted video using InnerTube API."
    upload_video(output_path, title, description, cookies_path)

if __name__ == "__main__":
    main()
