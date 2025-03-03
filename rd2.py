import os
import re
import requests

# Google API Configuration
API_KEY = "AIzaSyB4NaA2lMW6uZ6YjzbDCSo-he6zh_XBVkM"
CX_ID = "a73cae6bad04a492d"
SEARCH_API_URL = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CX_ID}&searchType=image"

# Directories
OUTPUT_DIR = "output"
IMAGES_DIR = "images"
CONTENT_DIR = "content"
PROMPT_DIR = "prompt"

# Ensure the images directory exists
if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

# Function to extract product names from the outputc.txt file
def extract_product_names_from_outputc(output_file_path):
    product_names = []
    try:
        with open(output_file_path, 'r') as file:
            output_text = file.read()

        # Regex to match numbered products with description (like 1. Product Name.)
        product_pattern = r"(\d+)\.(.*?)\s*[\.;:]"  # Matches 1. Product Name.
        matches = re.findall(product_pattern, output_text)
        for match in matches:
            product_name = match[1].strip()
            product_names.append(product_name)
    except Exception as e:
        print(f"Error reading outputc file {output_file_path}: {e}")
    return product_names

# Function to fetch 7 images for a given product name (for outputp.txt case)
def fetch_images_for_outputp(product_name):
    query = product_name
    url = f"{SEARCH_API_URL}&q={query}"

    try:
        response = requests.get(url)
        data = response.json()

        if "items" in data:
            # Fetch first 7 images
            for i, item in enumerate(data["items"][:7]):
                image_url = item['link']
                # Save image as images.png (replacing the same file)
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    image_path = os.path.join(IMAGES_DIR, "images.png")  # Save as images.png
                    with open(image_path, 'wb') as img_file:
                        img_file.write(image_response.content)
                    print(f"Saved image {i + 1} for product: {product_name}")
                else:
                    print(f"Failed to download image {i + 1} for product: {product_name}")
        else:
            print(f"No images found for product: {product_name}")
    except Exception as e:
        print(f"Error fetching images for {product_name}: {e}")

# Function to fetch 5 images for each product in outputc.txt
def fetch_images_for_outputc(product_name, index):
    query = product_name
    url = f"{SEARCH_API_URL}&q={query}"

    try:
        response = requests.get(url)
        data = response.json()

        if "items" in data:
            # Fetch first 5 images
            for i, item in enumerate(data["items"][:5]):
                image_url = item['link']
                # Save each image as 1.png, 2.png, etc. in the images folder
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    image_path = os.path.join(IMAGES_DIR, f"{index + i + 1}.png")
                    with open(image_path, 'wb') as img_file:
                        img_file.write(image_response.content)
                    print(f"Saved image {index + i + 1} for product: {product_name}")
                else:
                    print(f"Failed to download image {index + i + 1} for product: {product_name}")
        else:
            print(f"No images found for product: {product_name}")
    except Exception as e:
        print(f"Error fetching images for {product_name}: {e}")

# Main function to check for outputc.txt or outputp.txt and fetch images accordingly
def process_output_and_fetch_images():
    outputc_file_path = os.path.join(OUTPUT_DIR, "outputc.txt")
    outputp_file_path = os.path.join(OUTPUT_DIR, "outputp.txt")

    if os.path.exists(outputc_file_path):
        # If outputc.txt exists, process it
        print("Processing outputc.txt...")
        product_names = extract_product_names_from_outputc(outputc_file_path)
        if not product_names:
            print("No products found in outputc.txt.")
            return

        # Fetch 5 images for each product in outputc.txt
        for index, product_name in enumerate(product_names):
            print(f"Fetching images for product: {product_name}")
            fetch_images_for_outputc(product_name, index)

    elif os.path.exists(outputp_file_path):
        # If outputp.txt exists, fetch a single product's images
        print("Processing outputp.txt...")
        try:
            with open(outputp_file_path, 'r') as file:
                product_name = file.read().strip()

            if product_name:
                print(f"Fetching images for product: {product_name}")
                fetch_images_for_outputp(product_name)
            else:
                print("No product name found in outputp.txt.")
        except Exception as e:
            print(f"Error reading outputp.txt: {e}")

    else:
        print("No output files found (outputc.txt or outputp.txt).")

# Execute the process
if __name__ == "__main__":
    process_output_and_fetch_images()
