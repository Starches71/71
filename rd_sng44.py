
import praw
import os

# Reddit API credentials
client_id = 'LtRwJ6xsayuj8lRjSS5K_w'
client_secret = 'oGs66hSayCh0isCO9PwPyDHYhHoXMA'
refresh_token = '2109084143196-YJTf4ACDTKCk-Z4kUugCThQUmNl89Q'
user_agent = 'python:fetch_posts:v1.0 (by /u/Majestic_Computer_64)'

# Initialize Reddit API
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    refresh_token=refresh_token
)

# Directories
content_dir = "prd_content"
image_dir = "prd_images"
aff_link_dir = "prd_aff"

# List of subreddits to post in
subreddits = [
    "u/Majestic_Computer_64",  # Your profile
    "techtact",  # Your subreddit
    "Gadgets",
    "Coolgadgetstube",
    "Bestfindsgadgets",
    "Technology"
]

def get_first_file_content(directory):
    """ Get content from the first file found in a directory """
    files = sorted(os.listdir(directory))  # Sort to ensure consistency
    if not files:
        return None
    file_path = os.path.join(directory, files[0])
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().strip()

def get_image_files(directory):
    """ Get the list of image file paths in the directory """
    files = sorted(os.listdir(directory))
    return [os.path.join(directory, f) for f in files if f.endswith(('.jpg', '.png', '.jpeg'))][:5]  # Max 5 images

# Fetch content, images, and affiliate link
content = get_first_file_content(content_dir)
affiliate_link = get_first_file_content(aff_link_dir)
image_paths = get_image_files(image_dir)

# Extract title (first line of content)
title = content.split("\n")[0] if content else "Awesome Gadget You Must See!"

# Format the post body
post_body = f"{content}\n\nAffiliate Link: {affiliate_link}\n\n"

# Loop through each subreddit and post
for subreddit_name in subreddits:
    try:
        subreddit = reddit.subreddit(subreddit_name)
        
        if image_paths:
            print(f"Posting to r/{subreddit_name} with images...")
            post = subreddit.submit_gallery(
                title=title,
                images=[{"image_path": img} for img in image_paths]
            )
        else:
            print(f"Posting text to r/{subreddit_name}...")
            post = subreddit.submit(title=title, selftext=post_body)
        
        print(f"✅ Posted successfully to r/{subreddit_name}: {post.url}")
    
    except Exception as e:
        print(f"❌ Error posting to r/{subreddit_name}: {e}")
