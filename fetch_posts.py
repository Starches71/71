import praw
import requests
import os

# Reddit API credentials
client_id = 'LtRwJ6xsayuj8lRjSS5K_w'
client_secret = 'oGs66hSayCh0isCO9PwPyDHYhHoXMA'
refresh_token = '2109084143196-YJTf4ACDTKCk-Z4kUugCThQUmNl89Q'
user_agent = 'python:fetch_posts:v1.0 (by /u/your_username)'

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

# Fetch posts from subreddits
def fetch_posts():
    access_token = get_access_token()

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
        refresh_token=access_token
    )

    subreddits = ['Gadgets', 'Gadgetsindia', 'Coolgadgetstube', 'Bestfindsgadgets', 'Technology']
    posts_dir = './post'
    
    if not os.path.exists(posts_dir):
        os.makedirs(posts_dir)

    for subreddit_name in subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        
        for submission in subreddit.new(limit=10):  # Get the 10 latest posts
            post_data = {
                'title': submission.title,
                'url': submission.url,
                'score': submission.score,
                'comments': submission.num_comments,
                'created_utc': submission.created_utc,
            }

            # Save post to a file
            post_filename = os.path.join(posts_dir, f"{subreddit_name}_{submission.id}.txt")
            with open(post_filename, 'w') as post_file:
                post_file.write(str(post_data))

            print(f"Saved post: {post_filename}")

if __name__ == '__main__':
    fetch_posts()
