
import os
import requests
from urllib.parse import urlparse

# Google API credentials
API_KEY = "AIzaSyB4NaA2lMW6uZ6YjzbDCSo-he6zh_XBVkM"
CX_ID = "a73cae6bad04a492d"

# Directory and file paths
auto_dir = "auto"
ask_file = os.path.join(auto_dir, "ask.txt")  # Path to ask.txt
img_txt_file = os.path.join(auto_dir, "img.txt")  # Path to img.txt

# Ensure auto directory exists
os.makedirs(auto_dir, exist_ok=True)

# Read product name from ask.txt
if os.path.exists(ask_file):
    with open(ask_file, "r") as f:
        product_name = f.readline().strip()  # Read the first line (product name)
else:
    print(f"Error: {ask_file} not found!")
    exit()

# Modify search term to include "image" for fetching high-quality images
search_term = f"{product_name} image"
print(f"Search term: {search_term}")

# Google Custom Search API URL for images
url = f"https://www.googleapis.com/customsearch/v1?q={search_term}&searchType=image&key={API_KEY}&cx={CX_ID}&imgSize=huge"

# Make request to Google Custom Search API
response = requests.get(url)

# Check if the response was successful
if response.status_code == 200:
    data = response.json()

    # Extract the first image link
    if "items" in data and len(data["items"]) > 0:
        image_url = data["items"][0]["link"]
        print(f"Image URL from search result: {image_url}")

        # Get the file extension from the URL (i.e., .jpg, .png, etc.)
        file_extension = os.path.splitext(urlparse(image_url).path)[1]
        if not file_extension:
            print("Could not determine file extension from the URL.")
            exit()

        # Make a request to download the image
        img_data = requests.get(image_url).content

        # Save the image with the correct extension (e.g., .jpg, .jpeg)
        img_name = f"{product_name}{file_extension}"  # Product name with proper extension
        img_path = os.path.join(auto_dir, img_name)

        # Save the image
        with open(img_path, "wb") as img_file:
            img_file.write(img_data)

        print(f"Image saved as {img_path}")

        # Save the image URL to img.txt
        with open(img_txt_file, "w") as txt_file:
            txt_file.write(image_url + "\n")

        print(f"Image URL saved in {img_txt_file}")
    else:
        print("No image found in the API response.")
else:
    print(f"Failed to fetch data from Google Custom Search API. Status code: {response.status_code}")
