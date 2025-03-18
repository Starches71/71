
import praw
import os

# Reddit API credentials
client_id = 'LtRwJ6xsayuj8lRjSS5K_w'
client_secret = 'oGs66hSayCh0isCO9PwPyDHYhHoXMA'
refresh_token = '2109084143196-YJTf4ACDTKCk-Z4kUugCThQUmNl89Q'
user_agent = 'python:fetch_posts:v1.0 (by /u/Majestic_Computer_64)'

# Get access token using the refresh token
def get_access_token():
    url = 'https://www.reddit.com/api/v1/access_token'
    headers = {'User-Agent': user_agent}
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(url, data=data, headers=headers)
    response_data = response.json()
    access_token = response_data.get('access_token')
    return access_token

# Fetch content from post directory and post to Reddit
def post_to_reddit():
    access_token = get_access_token()

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
        refresh_token=access_token
    )

    # Define subreddit
    subreddit = reddit.subreddit('techtact')

    # Directory containing the posts
    posts_dir = './post'
    
    # Loop through all files in the post directory
    for post_filename in os.listdir(posts_dir):
        post_file_path = os.path.join(posts_dir, post_filename)
        
        with open(post_file_path, 'r') as post_file:
            # Read the content of the post
            content = post_file.read()

            # Split the content into title (first line) and body (rest of the content)
            lines = content.splitlines()
            title = lines[0]  # Title is the first line
            body = '\n'.join(lines[1:])  # The rest is the body

            # Submit the post to Reddit
            submission = subreddit.submit(title, selftext=body)
            print(f"Posted to Reddit: {title} - {submission.url}")

if __name__ == '__main__':
    post_to_reddit()
