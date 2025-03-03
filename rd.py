import os
import re
import requests
from groq import Groq
import time
import base64

# Initialize Groq client with your API key
client = Groq(api_key="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")

# Define the URL of the raw products.txt from GitHub
PRODUCTS_URL = "https://raw.githubusercontent.com/Starches71/71/main/products.txt"

# Define the path for the used products file
USED_PRODUCTS_FILE = "prd_used.txt"

# Your GitHub Personal Access Token (hardcoded)
GITHUB_TOKEN = "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"
REPO_OWNER = "Starches71"  # Replace with your GitHub username
REPO_NAME = "71"  # Replace with your GitHub repository name
FILE_PATH = "prd_used.txt"

# Define the content directory path
CONTENT_DIR = "content"

# Load products from the GitHub file
def load_products():
    try:
        response = requests.get(PRODUCTS_URL)
        if response.status_code == 200:
            products = response.text.splitlines()  # Split by new line
            print(f"Loaded {len(products)} products.")
            return products
        else:
            print("Failed to fetch products from GitHub.")
            return []
    except Exception as e:
        print(f"Error while fetching products: {e}")
        return []

# Save used product to prd_used.txt in the GitHub repository
def save_used_product_to_github(product):
    # Fetch the file from the repo to get its SHA
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        file_data = response.json()
        file_sha = file_data['sha']  # Get the file's SHA for updating
        # Read the current content of the file
        current_content = base64.b64decode(file_data['content']).decode()

        # Append the new product to the file content
        new_content = current_content + f"\n{product}"

        # Base64 encode the updated content
        encoded_content = base64.b64encode(new_content.encode()).decode()

        # Prepare the update data
        data = {
            "message": "Add new product to prd_used.txt",
            "content": encoded_content,
            "sha": file_sha
        }

        # Update the file in GitHub
        update_response = requests.put(url, json=data, headers=headers)

        if update_response.status_code == 200:
            print(f"Product '{product}' saved to GitHub repository {REPO_NAME}.")
        else:
            print(f"Failed to save product to GitHub: {update_response.status_code} - {update_response.text}")
    else:
        print(f"Failed to fetch the file: {response.status_code} - {response.text}")

# Remove numbers from the product name or category
def remove_numbers_from_product(product):
    # Use a regex to remove numbers and the periods following them
    cleaned_product = re.sub(r'^\d+\.\s*', '', product).strip()
    print(f"Cleaned product name: {cleaned_product}")
    return cleaned_product

# Query the LLM to check if the product is real or a category
def query_llm(product):
    prompt = f"Is the {product} a real product on Amazon or just a product category? Answer 'p' if it's a product, and answer 'c' if it's a product category. Just answer 'p' or 'c' only."
    conversation_history = [{"role": "user", "content": prompt}]
    
    try:
        completion = client.chat.completions.create(
            model="Llama-3.3-70b-Versatile",
            messages=conversation_history,
            temperature=0,
            max_tokens=1024,
            top_p=0,
            stream=False,
        )
        response_content = completion.choices[0].message.content if completion.choices else "No content found"
        print(f"LLM Response: {response_content}")
        return response_content.strip().lower()
    except Exception as e:
        print(f"Error while querying LLM: {e}")
        return None

# Save the product to a temporary file in the content directory
def save_product_to_content_dir(product):
    cleaned_product = remove_numbers_from_product(product)
    
    # Create content directory if it doesn't exist
    if not os.path.exists(CONTENT_DIR):
        os.makedirs(CONTENT_DIR)

    # Save product in content directory
    product_file_path = os.path.join(CONTENT_DIR, f"{cleaned_product}.txt")
    with open(product_file_path, 'w') as file:
        file.write(cleaned_product)
    print(f"Product saved to {product_file_path}")

# Save LLM response to a file in the content directory
def save_llm_response(product, response):
    cleaned_product = remove_numbers_from_product(product)
    
    # Save LLM response in content directory
    response_file_path = os.path.join(CONTENT_DIR, f"{cleaned_product}_response.txt")
    with open(response_file_path, 'w') as file:
        file.write(response)
    print(f"LLM response saved to {response_file_path}")

# Main function to run the process for a single product
def process_product():
    # Load products from products.txt
    products = load_products()

    if products:
        # Get the first product from the list
        product = products[0]
        print(f"Processing product: {product}")

        # Query the LLM and keep prompting until we get a valid response
        response = None
        while response not in ['p', 'c']:
            response = query_llm(product)
            if response not in ['p', 'c']:
                print(f"Invalid response '{response}', prompting again...")

        print(f"Response from LLM: {response}")
        
        # Save the used product to GitHub
        save_used_product_to_github(product)

        # Remove the product from the products list and save back to GitHub
        products = products[1:]  # Remove the first product
        update_products_file(products)

        # Save the product to the content directory
        save_product_to_content_dir(product)

        # Save the LLM response to the content directory
        save_llm_response(product, response)

        # Optionally, sleep to avoid rate-limiting issues
        time.sleep(2)
    else:
        print("No products available to process.")

# Update the products.txt file after removing the used product
def update_products_file(products):
    try:
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{PRODUCTS_URL.split('/')[-1]}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}

        # Get the current file data and SHA
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            file_data = response.json()
            file_sha = file_data['sha']
            current_content = base64.b64decode(file_data['content']).decode()

            # Rebuild the content by joining the remaining products
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

if __name__ == "__main__":
    process_product()
