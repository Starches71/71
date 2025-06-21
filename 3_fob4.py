
import os
import requests
from urllib.parse import quote_plus

# Your Amazon affiliate ID
affiliate_id = "starchestech-20"

# Input and output paths
product_file = "Vid/product_names.txt"
output_file = "auto/links.txt"
os.makedirs("auto", exist_ok=True)  # Ensure 'auto' directory exists

# Google API credentials
API_KEY = "AIzaSyB4NaA2lMW6uZ6YjzbDCSo-he6zh_XBVkM"
CX_ID = "a73cae6bad04a492d"

# Function to get affiliate link from Google search
def get_amazon_affiliate_link(product_name):
    search_term = f"{product_name} site:amazon.com"
    encoded_term = quote_plus(search_term)
    url = f"https://www.googleapis.com/customsearch/v1?q={encoded_term}&key={API_KEY}&cx={CX_ID}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for item in data.get("items", []):
                link = item.get("link", "")
                if "amazon.com" in link:
                    return f"{link}?tag={affiliate_id}"
            return "No Amazon link found"
        else:
            return f"API error {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

# Read all product names and generate affiliate links
if os.path.exists(product_file):
    with open(product_file, "r") as f:
        product_names = [line.strip() for line in f if line.strip()]
else:
    raise FileNotFoundError(f"{product_file} not found!")

# Process each product and save affiliate links
with open(output_file, "w") as out:
    for product in product_names:
        print(f"Searching: {product}")
        aff_link = get_amazon_affiliate_link(product)
        out.write(f"{product}: {aff_link}\n")
        print(f"Saved: {aff_link}")

print(f"\nAll affiliate links saved in: {output_file}")
