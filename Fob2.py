
import os
import requests
from urllib.parse import urlparse, parse_qs

# Google API credentials
API_KEY = "AIzaSyB4NaA2lMW6uZ6YjzbDCSo-he6zh_XBVkM"
CX_ID = "a73cae6bad04a492d"

# Directory and file names
auto_dir = "auto"
prd_aff_dir = "prd_aff"

# File paths
ask_file = os.path.join(auto_dir, "ask.txt")  # Assuming the file is named 'ask.txt'

# Read product name from ask.txt in the auto directory
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
    print("API Response:")
    print(data)  # Print the raw API response

    # Extract the first image link
    if "items" in data:
        first_result = data["items"][0]
        image_url = first_result["link"]
        image_title = first_result.get("title", "image")  # Get the image title, if available
        print(f"Image URL from search result: {image_url}")

        # Download the image in the highest quality
        try:
            img_data = requests.get(image_url).content
            img_name = f"{product_name}_image.jpg"  # Save the image with the product name
            image_path = os.path.join(prd_aff_dir, img_name)

            # Ensure the prd_aff directory exists
            if not os.path.exists(prd_aff_dir):
                os.makedirs(prd_aff_dir)

            with open(image_path, 'wb') as img_file:
                img_file.write(img_data)
            print(f"Image saved at {image_path}")
        except Exception as e:
            print(f"Failed to download the image: {e}")
    else:
        print("No image found in the API response.")
else:
    print(f"Failed to fetch data from Google Custom Search API. Status code: {response.status_code}")
