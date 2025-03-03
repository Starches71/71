
import os
import re
import requests
from groq import Groq
import time

# Initialize Groq client with your API key
client = Groq(api_key="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")

# Define the URL of the raw products.txt from GitHub
PRODUCTS_URL = "https://raw.githubusercontent.com/Starches71/71/main/products.txt"

# Define the path for the used products file
USED_PRODUCTS_FILE = "prd_used.txt"

# Define the directory for temporary product storage
TEMP_DIR = "rd"

# Define the directory for saving content (LLM responses)
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

# Save used product to prd_used.txt
def save_used_product(product):
    with open(USED_PRODUCTS_FILE, 'a') as file:
        file.write(f"{product}\n")
    print(f"Product '{product}' saved to {USED_PRODUCTS_FILE}.")

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
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
        )
        response_content = completion.choices[0].message.content if completion.choices else "No content found"
        print(f"LLM Response: {response_content}")
        return response_content.strip().lower()
    except Exception as e:
        print(f"Error while querying LLM: {e}")
        return None

# Create the temporary directory if it doesn't exist
def create_temp_dir():
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
        print(f"Created directory: {TEMP_DIR}")
    else:
        print(f"Directory {TEMP_DIR} already exists.")

# Create the content directory if it doesn't exist
def create_content_dir():
    if not os.path.exists(CONTENT_DIR):
        os.makedirs(CONTENT_DIR)
        print(f"Created directory: {CONTENT_DIR}")
    else:
        print(f"Directory {CONTENT_DIR} already exists.")

# Save the product to a temporary file in the rd directory
def save_product_to_temp_dir(product):
    cleaned_product = remove_numbers_from_product(product)
    product_file_path = os.path.join(TEMP_DIR, f"{cleaned_product}.txt")
    with open(product_file_path, 'w') as file:
        file.write(cleaned_product)
    print(f"Product saved to {product_file_path}")

# Save LLM response to a file in the content directory
def save_llm_response(product, response):
    cleaned_product = remove_numbers_from_product(product)
    response_file_path = os.path.join(CONTENT_DIR, f"{cleaned_product}_response.txt")
    with open(response_file_path, 'w') as file:
        file.write(response)
    print(f"LLM response saved to {response_file_path}")

# Main function to run the process
def process_products():
    products = load_products()
    if not products:
        print("No products found.")
        return

    # Create the necessary directories
    create_temp_dir()
    create_content_dir()

    for product in products:
        print(f"Processing product: {product}")
        
        # Query the LLM and keep prompting until we get a valid response
        response = None
        while response not in ['p', 'c']:
            response = query_llm(product)
            if response not in ['p', 'c']:
                print(f"Invalid response '{response}', prompting again...")

        print(f"Response from LLM: {response}")
        
        # Save the used product to prd_used.txt
        save_used_product(product)

        # Save the product to the temporary directory
        save_product_to_temp_dir(product)

        # Save the LLM response to the content directory
        save_llm_response(product, response)

        # Optionally, sleep to avoid rate-limiting issues
        time.sleep(2)

if __name__ == "__main__":
    process_products()
