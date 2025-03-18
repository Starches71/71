
import os
import google.auth
from google.auth.transport.requests import Request
from google.auth.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import subprocess
import yt_dlp

# YouTube API credentials
API_KEY = 'AIzaSyCOv3Fv5dPw9yDPKyssYo-Yz36HSJQdlqI'
CLIENT_ID = '60660374044-0s6mlj99gubn63vfuvbhgtkhuccbho7k.apps.googleusercontent.com'
CLIENT_SECRET = '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'
ACCESS_TOKEN = 'ya29.a0ARW5m77cCIkj33DKDm8WHPNcjiQMiCmFp87q-tjuUKrvmRgp1skWKWuAuCgf8JsHXwvbFyBU3WCVY0kvpT_HRPMsbZ23iX7mZjGOjwoUkmFEh9HbrE2sO0cwmX20y8wAbplemn9vMxq5EyEf___v5EZrg6-HRNklOHRKnpPMaCgYKAaQSARESFQHGX2MiXuq9zGU7VOC0mD4x2g2nDQ0175'
REFRESH_TOKEN = '1//03-eEOJR2u3uhCgYIARAAGAMSNwF-L9IrN5t3w8BfDMZ__bE1I7EDJckyWq9A0rNfXri-RUbSnzSnHmhHW5U_FuLFSGJ-WZHzVDs'

# Function to refresh the access token if it has expired
def refresh_access_token():
    credentials = Credentials(
        ACCESS_TOKEN,
        refresh_token=REFRESH_TOKEN,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
        print(f"Access token refreshed! New token: {credentials.token}")
        return credentials.token
    else:
        return credentials.token

# Authenticate and build the YouTube API client
def authenticate_youtube():
    credentials = Credentials(
        ACCESS_TOKEN,
        refresh_token=REFRESH_TOKEN,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )
    
    # Refresh the access token if necessary
    new_access_token = refresh_access_token()
    credentials.token = new_access_token

    youtube = build('youtube', 'v3', credentials=credentials)
    return youtube

# Function to download video using yt-dlp via torsocks (using Tor network)
def download_video():
    video_url = 'https://youtu.be/iT7zHrbm3q8?si=mGcf5RnkP_wjdcNv'  # New YouTube link
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'best_cheap_hotels_in_jeddah.mp4',
    }
    
    # Use torsocks to route yt-dlp through Tor
    command = ['torsocks', 'yt-dlp', video_url]
    subprocess.run(command, check=True)

# Upload video to YouTube
def upload_video(file_name, title, description, tags):
    youtube = authenticate_youtube()
    
    media = MediaFileUpload(file_name, mimetype='video/mp4', resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=dict(
            snippet=dict(
                title=title,
                description=description,
                tags=tags,
            ),
            status=dict(
                privacyStatus="public"  # You can change this to 'private' or 'unlisted'
            ),
        ),
        media_body=media
    )

    response = request.execute()
    print(f"Video uploaded successfully! Video ID: {response['id']}")

# Main function to run the entire process
def main():
    download_video()  # Download the video from YouTube via Tor
    upload_video(
        'best_cheap_hotels_in_jeddah.mp4',
        'Best Cheap Hotels in Jeddah',
        'This is a description for the Best Cheap Hotels in Jeddah video.',
        ['Jeddah', 'cheap hotels', 'best hotels in Jeddah']
    )  # Upload the downloaded video to YouTube

if __name__ == "__main__":
    main()
