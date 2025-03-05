import os
import requests
from urllib.parse import urlparse, parse_qs

# Google API credentials
API_KEY = "AIzaSyB4NaA2lMW6uZ6YjzbDCSo-he6zh_XBVkM"
CX_ID = "a73cae6bad04a492d"

# Directory and file names
prd_name_dir = "prd_name"
prd_aff_dir = "prd_aff"

# Read product name from prd_name directory
product_file = os.path.join(prd_name_dir, "product.txt")  # Assuming the file is named 'product.txt'

# Check if the product name file exists and read the product name
if os.path.exists(product_file):
    with open(product_file, "r") as f:
        product_name = f.readline().strip()  # Read the first line (product name)
else:
    print(f"Error: {product_file} not found!")
    exit()

# Modify search term to include "on amazon"
search_term = f"{product_name} on amazon"
print(f"Search term: {search_term}")

# Google Custom Search API URL
url = f"https://www.googleapis.com/customsearch/v1?q={search_term}&key={API_KEY}&cx={CX_ID}"

# Make request to Google Custom Search API
response = requests.get(url)

# Check if the response was successful
if response.status_code == 200:
    data = response.json()
    print("API Response:")
    print(data)  # Print the raw API response

    # Extract the first product link
    if "items" in data:
        first_result = data["items"][0]
        product_url = first_result["link"]
        print(f"Product URL from search result: {product_url}")
        
        # Check if the URL points to an Amazon product directly
        if "amazon.com" in product_url:
            print(f"Amazon product URL found: {product_url}")

            # Add affiliate ID to the URL
            affiliate_id = "starchestech-20"
            affiliate_link = f"{product_url}?tag={affiliate_id}"

            # Ensure prd_aff directory exists
            if not os.path.exists(prd_aff_dir):
                os.makedirs(prd_aff_dir)

            # Save the affiliate link to a file
            affiliate_link_file = os.path.join(prd_aff_dir, "affiliate_link.txt")
            with open(affiliate_link_file, "w") as f:
                f.write(affiliate_link)

            print(f"Affiliate link saved at {affiliate_link_file}")
            print(f"Affiliate link: {affiliate_link}")
        else:
            print("No direct Amazon URL found in the search result.")
    else:
        print("No items found in the API response.")
else:
    print(f"Failed to fetch data from Google Custom Search API. Status code: {response.status_code}")
