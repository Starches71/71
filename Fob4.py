
import os
import requests
from urllib.parse import quote_plus

# Your affiliate ID
affiliate_id = "starchestech-20"

# Directory and file names
auto_dir = "auto"
ask_file = os.path.join(auto_dir, "ask.txt")

# Google API credentials
API_KEY = "AIzaSyB4NaA2lMW6uZ6YjzbDCSo-he6zh_XBVkM"
CX_ID = "a73cae6bad04a492d"

# Function to search for the product on Amazon using Google Custom Search
def get_amazon_affiliate_link(product_name):
    search_term = f"{product_name} on amazon"
    search_term_encoded = quote_plus(search_term)  # URL encode the search term

    # Google Custom Search API URL
    url = f"https://www.googleapis.com/customsearch/v1?q={search_term_encoded}&key={API_KEY}&cx={CX_ID}"

    # Make the API request to search for the product
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # Check if items are returned in the response
        if "items" in data:
            first_result = data["items"][0]
            product_url = first_result["link"]
            print(f"Product URL from search result: {product_url}")

            # Check if the URL is an Amazon link
            if "amazon.com" in product_url:
                # Create the affiliate link by appending the affiliate ID
                affiliate_link = f"{product_url}?tag={affiliate_id}"

                # Save the affiliate link to a file in the 'auto' directory
                affiliate_link_file = os.path.join(auto_dir, "link.txt")
                with open(affiliate_link_file, "w") as f:
                    f.write(affiliate_link)

                print(f"Affiliate link saved: {affiliate_link}")
                return affiliate_link
            else:
                print("The search result is not an Amazon link.")
        else:
            print("No products found in the search results.")
    else:
        print(f"Failed to fetch data from Google Custom Search API. Status code: {response.status_code}")
    return None

# Read the product name from the ask.txt file in the 'auto' directory
if os.path.exists(ask_file):
    with open(ask_file, "r") as f:
        product_name = f.readline().strip()  # Read the first line (product name)
    print(f"Product name from ask.txt: {product_name}")

    # Get the Amazon affiliate link for the product
    affiliate_link = get_amazon_affiliate_link(product_name)
else:
    print(f"Error: {ask_file} not found!")
