
import requests

# Updated YouTube video ID
video_id = 'lv0jJtMW58k'  # Extract the video ID from the URL
url = 'https://yt-api.p.rapidapi.com/dl'
querystring = {'id': video_id, 'cgeo': 'DE'}

headers = {
    'x-rapidapi-key': '00181c98c6mshb28efee02d1aa4cp101a3bjsn810e9f1a5717',
    'x-rapidapi-host': 'yt-api.p.rapidapi.com'
}

response = requests.get(url, headers=headers, params=querystring)

# Check the response status
if response.status_code == 200:
    response_json = response.json()
    print("Response JSON:", response_json)

    # Extract video download URL if it exists
    if 'url' in response_json:
        download_url = response_json['url']
        print(f'Download URL: {download_url}')
    else:
        # If the 'url' isn't in the main response, try extracting from a different part
        playback_url = None
        if 'formats' in response_json:
            for format in response_json['formats']:
                if 'url' in format:
                    playback_url = format['url']
                    break

        if playback_url:
            print(f'Found Download URL: {playback_url}')
        else:
            print('Download URL not found in response.')
else:
    print(f'Failed to get video. Status code: {response.status_code}')
