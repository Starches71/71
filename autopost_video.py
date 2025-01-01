import subprocess
import sys
import yt_dlp
import requests
import json
import os

# Check if yt-dlp is installed, if not, install it
try:
    import yt_dlp
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])

# Download video using yt-dlp
def download_video(url, output_path):
    ydl_opts = {
        'outtmpl': output_path,  # Download path template
        'noplaylist': True,  # Ensure single video download
        'format': 'bestvideo+bestaudio/best',  # Best video + audio quality
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Upload video via InnerTube (YouTube API)
def upload_video(video_path, title, description, cookie_url, context):
    # Download the cookies.txt from GitHub URL
    cookies_content = requests.get(cookie_url).text

    # Prepare headers and other necessary parameters
    headers = {
        'User-Agent': context['client']['userAgent'],
        'Content-Type': 'application/json',
    }

    # Prepare InnerTube upload parameters
    upload_url = 'https://upload.youtube.com/upload/your_video_upload_endpoint'  # Replace with actual endpoint
    video_data = {
        "title": title,
        "description": description,
        "tags": ['random', 'video', 'yt-dlp'],
        "privacyStatus": "public",  # Can be "private", "unlisted", or "public"
        "file": open(video_path, 'rb'),  # Open the downloaded video
        "thumbnail": None,  # No thumbnail
        "cookies": cookies_content,
    }
    
    # Send the upload request
    response = requests.post(upload_url, headers=headers, data=json.dumps(video_data))
    
    if response.status_code == 200:
        print(f"Video uploaded successfully: {title}")
    else:
        print(f"Failed to upload video: {response.status_code}, {response.text}")

# Main function to combine downloading and uploading
def main():
    # Download a random 10-sec YouTube video
    video_url = 'https://youtu.be/s7yBWncUrI0'
    output_path = 'random_video.mp4'  # Save the video as random_video.mp4
    
    # Download the video
    download_video(video_url, output_path)
    
    # Title and description for the video
    title = "Random 10 sec Video"
    description = "This is a random 10-second video downloaded using yt-dlp and uploaded via InnerTube."

    # GitHub URL for cookies.txt
    cookie_url = 'https://raw.githubusercontent.com/your-username/your-repo/main/cookies.txt'  # Replace with actual URL

    # InnerTube context
    context = {
        'client': {
            'userAgent': 'com.google.android.apps.youtube.creator/24.45.100 (Linux; U; Android 11) gzip',
            'clientName': 'ANDROID_CREATOR',
            'clientVersion': '24.45.100',
            'androidSdkVersion': 30,
            'osName': 'Android',
            'osVersion': '11',
        },
        'INNERTUBE_CONTEXT': {
            'client': {
                'clientName': 'ANDROID_CREATOR',
                'clientVersion': '24.45.100',
                'androidSdkVersion': 30,
                'userAgent': 'com.google.android.apps.youtube.creator/24.45.100 (Linux; U; Android 11) gzip',
                'osName': 'Android',
                'osVersion': '11',
            },
        },
        'INNERTUBE_CONTEXT_CLIENT_NAME': 14,
        'REQUIRE_JS_PLAYER': False,
        'REQUIRE_PO_TOKEN': True,
        'REQUIRE_AUTH': True,
    }

    # Upload the downloaded video
    upload_video(output_path, title, description, cookie_url, context)

# Run the script
if __name__ == '__main__':
    main()