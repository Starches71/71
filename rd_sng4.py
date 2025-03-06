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
    "techtact",
    "Coolgadgetstube",
    "Bestfindsgadgets",
    "Technology"
]

def get_first_file_content(directory):
    """ Get content from the first file found in a directory """
    files = sorted(os.listdir(directory))
    if not files:
        return None
    file_path = os.path.join(directory, files[0])
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().strip()

def get_image_files(directory):
    """ Get the list of image file paths in the directory """
    files = sorted(os.listdir(directory))
    return [os.path.join(directory, f) for f in files if f.endswith(('.jpg', '.png', '.jpeg'))][:1]  # Take only 1 image

# Fetch content, images, and affiliate link
content = get_first_file_content(content_dir)
affiliate_link = get_first_file_content(aff_link_dir)
image_paths = get_image_files(image_dir)

# Ensure content is present
if content:
    title = content.split("\n")[0]
    body = "\n".join(content.split("\n")[1:])
else:
    title = "Awesome Gadget You Must See!"
    body = "Check out this amazing gadget!"

# Ensure affiliate link is added to the body
post_body = f"{body}\n\nAffiliate Link: {affiliate_link}" if affiliate_link else body

# Debug: Print the content to check for issues
print(f"Title: {title}")
print(f"Body: {post_body}")
print(f"Affiliate Link: {affiliate_link}")

# Loop through each subreddit and post
for subreddit_name in subreddits:
    try:
        subreddit = reddit.subreddit(subreddit_name)
        
        # Post with image if image paths are available
        if image_paths:
            print(f"Posting to r/{subreddit_name} with an image...")
            image_path = image_paths[0]
            
            # Create an image post (without selftext)
            post = subreddit.submit_image(
                title=title,
                image_path=image_path
            )
            
            print(f"✅ Posted successfully to r/{subreddit_name}: {post.url}")
            
            # Add body text as a comment under the post
            comment_text = post_body.strip()
            if comment_text:
                post.reply(comment_text)
                print(f"📝 Added comment with details to r/{subreddit_name}")

        # If no image is available, post text content
        else:
            print(f"Posting text to r/{subreddit_name}...")
            
            # Create a text post
            post = subreddit.submit(
                title=title,
                selftext=post_body
            )
            
            print(f"✅ Posted successfully to r/{subreddit_name}: {post.url}")
    
    except Exception as e:
        print(f"❌ Error posting to r/{subreddit_name}: {e}")
