import os
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from yt_dlp import YoutubeDL

# Function to download video
def download_video(url, output_path):
    ydl_opts = {
        'outtmpl': output_path,
        'noplaylist': True,
        'format': 'bestvideo+bestaudio/best',
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Function to upload video via YouTube Data API
def upload_video(file_path, title, description, access_token, refresh_token):
    # Set up credentials using access and refresh tokens
    creds = Credentials(
        token=access_token,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id="60660374044-78lne6ja6mate7ggitngnhb6nvths0h5.apps.googleusercontent.com",
        client_secret="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",
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )

    # Build the YouTube service
    youtube = build('youtube', 'v3', credentials=creds)

    # Prepare the video for upload
    media = MediaFileUpload(file_path, resumable=True, mimetype='video/*')

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": ["auto-upload", "YouTube API"],
                "categoryId": "22"  # Category ID for 'People & Blogs'
            },
            "status": {
                "privacyStatus": "private"  # Set to 'public' or 'unlisted' if needed
            }
        },
        media_body=media
    )

    # Upload the video
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploading... {int(status.progress() * 100)}%")

    print("Upload completed!")
    print(f"Video URL: https://www.youtube.com/watch?v={response['id']}")

# Main function
def main():
    video_url = "https://youtu.be/s7yBWncUrI0"  # Replace with your desired video URL
    output_path = "downloaded_video.mp4"

    # Your OAuth tokens
    access_token = "ya29.a0ARW5m77cCIkj33DKDm8WHPNcjiQMiCmFp87q-tjuUKrvmRgp1skWKWuAuCgf8JsHXwvbFyBU3WCVY0kvpT_HRPMsbZ23iX7mZjGOjwoUkmFEh9HbrE2sO0cwmX20y8wAbplemn9vMxq5EyEf___v5EZrg6-HRNklOHRKnpPMaCgYKAaQSARESFQHGX2MiXuq9zGU7VOC0mD4x2g2nDQ0175"
    refresh_token = "1//03-eEOJR2u3uhCgYIARAAGAMSNwF-L9IrN5t3w8BfDMZ__bE1I7EDJckyWq9A0rNfXri-RUbSnzSnHmhHW5U_FuLFSGJ-WZHzVDs"

    # Step 1: Download video
    print("Downloading video...")
    download_video(video_url, output_path)

    # Step 2: Upload video
    print("Uploading video...")
    title = "Random 10-second video"
    description = "This is an auto-posted video using YouTube API."
    upload_video(output_path, title, description, access_token, refresh_token)

if __name__ == "__main__":
    main()
