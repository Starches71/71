
import os
import base64
import requests
import sys
import time
from groq import Groq

# Hardcoded API keys
GITHUB_TOKEN = "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"  # Your GitHub personal access token
GROQ_API_KEY = "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"  # Your Groq API key

if not GITHUB_TOKEN or not GROQ_API_KEY:
    print("❌ API keys are missing. Please provide valid GitHub and Groq API keys.")
    sys.exit(1)

# GitHub repository details
REPO_OWNER = "Starches71"
REPO_NAME = "71"
PRODUCTS_FILE_PATH = "products.txt"
USED_PRODUCTS_FILE_PATH = "prd_used.txt"
C_FILE = "c.txt"
P_FILE = "p.txt"
MAX_PRODUCTS = 50  # Process up to 50 products

# URL for the raw products.txt
PRODUCTS_URL = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/{PRODUCTS_FILE_PATH}"
USED_PRODUCTS_URL = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/{USED_PRODUCTS_FILE_PATH}"

# Groq API setup using Groq Python client
client = Groq(api_key=GROQ_API_KEY)

# Function to fetch products from GitHub
def load_products():
    try:
        response = requests.get(PRODUCTS_URL)
        if response.status_code == 200:
            products = response.text.splitlines()
            print(f"Loaded {len(products)} products.")
            return products
        else:
            print("Failed to fetch products from GitHub.")
            return []
    except Exception as e:
        print(f"Error while fetching products: {e}")
        return []

# Function to save used product to GitHub repository
def save_used_product_to_github(product):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{USED_PRODUCTS_FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            file_data = response.json()
            file_sha = file_data['sha']
            current_content = base64.b64decode(file_data['content']).decode()

            new_content = current_content + f"\n{product}"

            encoded_content = base64.b64encode(new_content.encode()).decode()

            data = {
                "message": "Add new product to prd_used.txt",
                "content": encoded_content,
                "sha": file_sha
            }

            update_response = requests.put(url, json=data, headers=headers)

            if update_response.status_code == 200:
                print(f"Product '{product}' saved to GitHub repository {REPO_NAME}.")
            else:
                print(f"Failed to save product to GitHub: {update_response.status_code} - {update_response.text}")
        else:
            print(f"Failed to fetch the file: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error while updating GitHub file: {e}")

# Function to remove product from products.txt and update it on GitHub
def update_products_file(products):
    try:
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{PRODUCTS_FILE_PATH}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            file_data = response.json()
            file_sha = file_data['sha']
            current_content = base64.b64decode(file_data['content']).decode()

            # Remove the processed product
            new_content = "\n".join(products)
            encoded_content = base64.b64encode(new_content.encode()).decode()

            data = {
                "message": "Remove used product from products.txt",
                "content": encoded_content,
                "sha": file_sha
            }

            update_response = requests.put(url, json=data, headers=headers)
            if update_response.status_code == 200:
                print("products.txt updated successfully.")
            else:
                print(f"Failed to update products.txt: {update_response.status_code}")
        else:
            print(f"Failed to fetch products file from GitHub: {response.status_code}")
    except Exception as e:
        print(f"Error while updating products file: {e}")

# Function to classify product via Groq API using the Groq Python client
def classify_product(product):
    try:
        # Making the Groq request using the new API format
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": product}],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )

        category = None
        # Loop through the Groq response chunks to check for content
        for chunk in completion:
            response_content = chunk.choices[0].delta.content
            if response_content:
                print(f"Groq Response: {response_content}")
                # Check if the response contains 'p' or 'c' category
                if "p" in response_content.lower():
                    category = "p"
                elif "c" in response_content.lower():
                    category = "c"

        if category:
            print(f"Product classified as: {category}")
            return category
        else:
            print(f"Failed to classify '{product}'.")
            return None

    except Exception as e:
        print(f"Error while querying Groq: {e}")
        return None

# Function to save product to the appropriate file
def save_to_file(product, category):
    if category == "p":
        with open(P_FILE, "a") as f:
            f.write(product + "\n")
        print(f"Product '{product}' classified as 'p' and saved to {P_FILE}.")
    elif category == "c":
        with open(C_FILE, "a") as f:
            f.write(product + "\n")
        print(f"Product '{product}' classified as 'c' and saved to {C_FILE}.")

# Main function to process the products
def process_products():
    products = load_products()
    if not products:
        print("No products to process.")
        return

    products_processed = 0

    for product in products[:MAX_PRODUCTS]:
        print(f"Processing product {products_processed + 1}: {product}")
        category = classify_product(product)

        if category:
            save_to_file(product, category)
            save_used_product_to_github(product)
            
            # Remove the processed product from the list
            products.remove(product)
            update_products_file(products)

            products_processed += 1

        if products_processed >= MAX_PRODUCTS:
            break

        time.sleep(1)  # Sleep to avoid rate limiting issues

    print("✅ Done processing products.")

if __name__ == "__main__":
    process_products()
