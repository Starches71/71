
import os
import requests
import time
from datetime import datetime, timedelta

# Your credentials
PAGE_ID = "577411745457265"  # Your Page ID
APP_ID = "1717471989199733"  # Your App ID
APP_SECRET = "4dd9e1a03e3d5413347d9e3469eafd88"  # Your App Secret
ACCESS_TOKEN = "EAAYaCBvT83UBOziasqgAPPHaNQHZCYZCW4B9dMNNDJbRwn1rrSmoeauxd6ERTXNZBCivKt2rDpkFSBiQIP99offXoGSyvCC3sdRqXRi2FgRqmYoZBxVRUOSrFUbkZADZB9MlCeUdw6DwN0fPWryEzZBfaREp6tepfZA8r0j7DYMZCZCDuMwK8x1G4vU4OwvPdOP7IeuM3ltRTQ"  # Replace with your real long-term token

# Directory and file paths
AUTO_DIR = "auto"
IMG_FILE_EXTENSIONS = ['.jpeg', '.jpg', '.png', '.gif']  # Define image file types to search for
HASHTAG_FILE = os.path.join(AUTO_DIR, "hashtag.txt")
TITLE_FILE = os.path.join(AUTO_DIR, "tittle.txt")
BODY_FILE = os.path.join(AUTO_DIR, "body.txt")
LINK_FILE = os.path.join(AUTO_DIR, "link.txt")
URL_FILE = os.path.join(AUTO_DIR, "url.txt")  # New path to the image URL

# Function to read content from a file
def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readline().strip()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

# Function to get the image URL from the auto/url.txt
def get_image_url():
    try:
        # Check if the URL file exists and read it
        if os.path.exists(URL_FILE):
            with open(URL_FILE, 'r') as file:
                return file.readline().strip()  # Read the URL
        else:
            print(f"Error: {URL_FILE} not found!")
            return None
    except Exception as e:
        print(f"Error reading {URL_FILE}: {e}")
        return None

# Function to post the message to Facebook with an image URL
def post_to_facebook(title, body, link, image_url):
    url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/feed"
    message = f"{title}\n\nView product\n[{link}]"
    payload = {
        "message": message + "\n\n" + body,  # Title and body of the post
        "access_token": ACCESS_TOKEN,
        "link": image_url  # Include the image URL in the post
    }
    response = requests.post(url, data=payload)
    result = response.json()

    if "id" in result:
        print(f"Post successful! Post ID: {result['id']}")
        return result["id"]
    else:
        print(f"Failed to post: {result}")
        return None

# Function to post the first comment with the affiliate link
def post_first_comment(post_id, link):
    url = f"https://graph.facebook.com/v19.0/{post_id}/comments"
    comment = f"View product\n{link}"
    payload = {
        "message": comment,
        "access_token": ACCESS_TOKEN
    }
    response = requests.post(url, data=payload)
    result = response.json()

    if "id" in result:
        print(f"First comment posted successfully! Comment ID: {result['id']}")
    else:
        print(f"Failed to post comment: {result}")

# Main function to execute the process
def main():
    # Read content from the files in the auto directory
    title = read_file(TITLE_FILE)
    body = read_file(BODY_FILE)
    link = read_file(LINK_FILE)
    image_url = get_image_url()  # Get the image URL from auto/url.txt
    hashtags = read_file(HASHTAG_FILE)  # Hashtags, if needed later
    
    if title and body and link:
        # If an image URL is found, use it for your post
        if image_url:
            print(f"Image URL found: {image_url}")
        else:
            print("No image URL found in the auto/url.txt file.")
        
        # Post to Facebook
        post_id = post_to_facebook(title, body, link, image_url)

        if post_id:
            # Post the first comment with the affiliate link
            post_first_comment(post_id, link)
    else:
        print("Required content is missing in one or more files.")

if __name__ == "__main__":
    main()
