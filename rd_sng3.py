
import os
from playwright.sync_api import sync_playwright

# Amazon Affiliate ID
affiliate_id = "starchestech-20"

# Directory and file names
prd_name_dir = "prd_name"
prd_aff_dir = "prd_aff"

# Read product name from prd_name directory
product_file = os.path.join(prd_name_dir, "product_name.txt")

# Check if the product name file exists and read the product name
if os.path.exists(product_file):
    with open(product_file, "r") as f:
        product_name = f.readline().strip()  # Read the first line (product name)
else:
    print(f"Error: {product_file} not found!")
    exit()

# Modify search term to include "on amazon"
search_term = f"{product_name} on amazon"
search_url = f"https://www.amazon.com/s?k={search_term.replace(' ', '+')}"

# Start Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Run in headless mode
    page = browser.new_page()
    
    # Go to Amazon search page
    page.goto(search_url)
    
    # Wait for the search results to load (you can customize the wait condition here)
    page.wait_for_selector('a.a-link-normal')
    
    # Extract the first product link
    product_link = page.query_selector('a.a-link-normal')
    if product_link:
        product_url = product_link.get_attribute('href')
        
        # Add affiliate ID to the URL
        affiliate_link = f"{product_url}?tag={affiliate_id}"

        # Ensure prd_aff directory exists
        if not os.path.exists(prd_aff_dir):
            os.makedirs(prd_aff_dir)

        # Save the affiliate link to a file
        affiliate_link_file = os.path.join(prd_aff_dir, "affiliate_link.txt")
        with open(affiliate_link_file, "w") as f:
            f.write(affiliate_link)

        print(f"Affiliate link saved at {affiliate_link_file}")
    else:
        print("No product link found.")
    
    browser.close()
