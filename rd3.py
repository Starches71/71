
import os
import requests
import re

# Define Directories
OUTPUT_DIR = "output"
IMAGES_DIR = "images"
CONTENT_DIR = "content"
AFF_DIR = "aff"
PROMPT_DIR = "prompt"

# Ensure the 'aff' directory exists
if not os.path.exists(AFF_DIR):
    os.makedirs(AFF_DIR)

# Your Amazon Affiliate ID
AFFILIATE_ID = "starchestech-20"

# Function to clean the URL and add the affiliate ID
def create_affiliate_link(url):
    # Remove any extra parameters from the URL
    clean_url = re.sub(r'(&?)([a-zA-Z0-9_=-]+)(&?)([a-zA-Z0-9_=-]+)?$', '', url)
    # Add affiliate ID to the link
    affiliate_link = f"{clean_url}&tag={AFFILIATE_ID}"
    return affiliate_link

# Function to search for product on Google and get the first Amazon link
def get_amazon_affiliate_link(product_name):
    search_query = f"{product_name} on amazon"
    google_search_url = f"https://www.google.com/search?q={search_query}"

    try:
        response = requests.get(google_search_url)
        if response.status_code == 200:
            # Extract the first Amazon link from the search results
            amazon_link_pattern = r"(https://www\.amazon\.com/[^\s]+)"
            amazon_link_match = re.search(amazon_link_pattern, response.text)
            
            if amazon_link_match:
                amazon_url = amazon_link_match.group(0)
                affiliate_url = create_affiliate_link(amazon_url)
                return affiliate_url
            else:
                print(f"No Amazon link found for product: {product_name}")
        else:
            print(f"Failed to search for {product_name}")
    except Exception as e:
        print(f"Error while fetching the Amazon link for {product_name}: {e}")
    
    return None

# Function to process outputp.txt and fetch the Amazon link for the product
def process_outputp_and_generate_affiliate_link():
    outputp_file_path = os.path.join(OUTPUT_DIR, "outputp.txt")
    
    if os.path.exists(outputp_file_path):
        print("Processing outputp.txt...")
        try:
            with open(outputp_file_path, 'r') as file:
                product_name = file.read().strip()

            if product_name:
                print(f"Fetching Amazon link for product: {product_name}")
                affiliate_link = get_amazon_affiliate_link(product_name)
                
                if affiliate_link:
                    aff_file_path = os.path.join(AFF_DIR, "amazon_link.aff")
                    with open(aff_file_path, 'w') as aff_file:
                        aff_file.write(affiliate_link)
                    print(f"Affiliate link saved for product: {product_name}")
                else:
                    print(f"Could not fetch affiliate link for product: {product_name}")
            else:
                print("No product name found in outputp.txt.")
        except Exception as e:
            print(f"Error reading outputp.txt: {e}")
    else:
        print("No outputp.txt file found.")

# Function to process outputc.txt and generate affiliate links for multiple products
def process_outputc_and_generate_affiliate_links():
    outputc_file_path = os.path.join(OUTPUT_DIR, "outputc.txt")
    
    if os.path.exists(outputc_file_path):
        print("Processing outputc.txt...")
        
        try:
            with open(outputc_file_path, 'r') as file:
                output_text = file.read()

            # Regex to match numbered products (like 1. Samsung XYZ)
            product_pattern = r"(\d+)\.(.*?)\s*[\.;:]"  # Matches 1. Product Name.
            matches = re.findall(product_pattern, output_text)
            
            # For each product, fetch the affiliate link and save it
            for index, match in enumerate(matches):
                product_name = match[1].strip()
                print(f"Fetching Amazon link for product: {product_name}")
                affiliate_link = get_amazon_affiliate_link(product_name)
                
                if affiliate_link:
                    aff_file_path = os.path.join(AFF_DIR, f"{index + 1}.aff")
                    with open(aff_file_path, 'w') as aff_file:
                        aff_file.write(affiliate_link)
                    print(f"Affiliate link saved for product: {product_name}")
                else:
                    print(f"Could not fetch affiliate link for product: {product_name}")
        except Exception as e:
            print(f"Error reading outputc.txt: {e}")
    else:
        print("No outputc.txt file found.")

# Main function to process the output files
def process_output_and_generate_affiliate_links():
    outputp_file_path = os.path.join(OUTPUT_DIR, "outputp.txt")
    outputc_file_path = os.path.join(OUTPUT_DIR, "outputc.txt")
    
    if os.path.exists(outputp_file_path):
        # Process outputp.txt
        process_outputp_and_generate_affiliate_link()
    
    elif os.path.exists(outputc_file_path):
        # Process outputc.txt
        process_outputc_and_generate_affiliate_links()
    
    else:
        print("No output files found (outputp.txt or outputc.txt).")

# Run the process
if __name__ == "__main__":
    process_output_and_generate_affiliate_links()
