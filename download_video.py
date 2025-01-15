
import requests
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Function to download video from the download URL
def download_video(download_url, output_path):
    response = requests.get(download_url, stream=True)
    if response.status_code == 200:
        with open(output_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Video downloaded successfully to {output_path}")
    else:
        print(f"Failed to download video. Status code: {response.status_code}")

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
    # Video details
    video_id = 'lv0jJtMW58k'  # Replace with your desired video ID
    url = 'https://yt-api.p.rapidapi.com/dl'
    querystring = {'id': video_id, 'cgeo': 'DE'}

    headers = {
        'x-rapidapi-key': '00181c98c6mshb28efee02d1aa4cp101a3bjsn810e9f1a5717',
        'x-rapidapi-host': 'yt-api.p.rapidapi.com'
    }

    # Fetch the video download URL from RapidAPI
    response = requests.get(url, headers=headers, params=querystring)

    # Check if the API request was successful
    if response.status_code == 200:
        response_json = response.json()
        print("Response JSON:", response_json)

        # Extract the download URL
        if 'url' in response_json:
            download_url = response_json['url']
            print(f'Download URL: {download_url}')
        else:
            # If the 'url' isn't found, try getting it from a different part of the response
            playback_url = None
            if 'formats' in response_json:
                for format in response_json['formats']:
                    if 'url' in format:
                        playback_url = format['url']
                        break

            if playback_url:
                download_url = playback_url
                print(f'Found Download URL: {download_url}')
            else:
                print('Download URL not found in response.')
                return  # Exit if no download URL found
    else:
        print(f'Failed to get video. Status code: {response.status_code}')
        return  # Exit if API call failed

    # Step 2: Download video
    output_path = "downloaded_video.mp4"
    print("Downloading video...")
    download_video(download_url, output_path)

    # Step 3: Upload video to YouTube
    title = "Random 10-second video"
    description = "This is an auto-posted video using YouTube API."
    access_token = "YOUR_ACCESS_TOKEN"  # Replace with your actual access token
    refresh_token = "YOUR_REFRESH_TOKEN"  # Replace with your actual refresh token
    print("Uploading video...")
    upload_video(output_path, title, description, access_token, refresh_token)

if __name__ == "__main__":
    main()
