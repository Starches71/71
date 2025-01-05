
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
    # Print the entire response JSON to inspect its structure
    response_json = response.json()
    print("Response JSON:", response_json)

    # Attempt to find the download URL
    download_url = response_json.get('url')
    if download_url:
        print(f'Download URL: {download_url}')
    else:
        print('Download URL not found in response.')
else:
    print(f'Failed to get video. Status code: {response.status_code}')
