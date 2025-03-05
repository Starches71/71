
import os
import requests

# Replace with your API key and Search Engine ID
API_KEY = "AIzaSyB4NaA2lMW6uZ6YjzbDCSo-he6zh_XBVkM"
CX_ID = "a73cae6bad04a492d"

# Read the product name from the file in the prd_name directory
prd_name_dir = "prd_name"
product_file = os.path.join(prd_name_dir, "product_name.txt")  # Assuming the file name is product_name.txt

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

# Extract image links and save images
if "items" in data:
    for i, item in enumerate(data["items"][:5]):  # Get first 5 images
        image_url = item['link']
        image_name = f"{output_dir}/image_{i+1}.jpg"

        # Download and save image
        try:
            img_data = requests.get(image_url).content
            with open(image_name, 'wb') as f:
                f.write(img_data)
            print(f"Image {i+1} saved as {image_name}")
        except Exception as e:
            print(f"Failed to download image {i+1}: {e}")
else:
    print("No images found.")
