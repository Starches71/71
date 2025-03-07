
import os
import requests

# Replace with your API key and Search Engine ID
API_KEY = "AIzaSyB4NaA2lMW6uZ6YjzbDCSo-he6zh_XBVkM"
CX_ID = "a73cae6bad04a492d"

# Read the product name from the file in the prd_name directory
prd_name_dir = "prd_name"
product_file = os.path.join(prd_name_dir, "product.txt")  # Adjusted file name to "product.txt"

# Check if the file exists and read the product name
if os.path.exists(product_file):
    with open(product_file, "r") as f:
        QUERY = f.readline().strip()  # Read the first line (product name)
else:
    print(f"Error: {product_file} not found!")
    exit()

# Google Custom Search API URL
url = f"https://www.googleapis.com/customsearch/v1?q={QUERY}&key={API_KEY}&cx={CX_ID}&searchType=image"

# Make request
response = requests.get(url)
data = response.json()

# Ensure prd_images directory exists
output_dir = "prd_images"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# File to save the image links
image_links_file = os.path.join(output_dir, "image_links.txt")

# Extract image links and save them to a file
if "items" in data:
    with open(image_links_file, 'w') as f:
        for i, item in enumerate(data["items"][:5]):  # Get first 5 image links
            image_url = item['link']
            f.write(image_url + "\n")  # Write the image URL to the file
            print(f"Image link {i+1} saved: {image_url}")
else:
    print("No images found.")
