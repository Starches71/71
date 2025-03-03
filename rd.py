import os
import requests
from groq import Groq
import time

# Initialize Groq client with your API key
client = Groq(api_key="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")

# Define the URL of the raw products.txt from GitHub
PRODUCTS_URL = "https://raw.githubusercontent.com/Starches71/71/main/products.txt"

# Define the path for the used products file
USED_PRODUCTS_FILE = "prd_used.txt"

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

# Main function to run the process
def process_products():
    products = load_products()
    if not products:
        print("No products found.")
        return

    for product in products:
        print(f"Processing product: {product}")
        
        # Query the LLM
        response = query_llm(product)
        
        if response:
            print(f"Response from LLM: {response}")
            if response == 'p':  # If it's a product
                print(f"{product} is a real product.")
            elif response == 'c':  # If it's a category
                print(f"{product} is a product category.")
            else:
                print(f"Unexpected response: {response}")
            
            # Save the used product to prd_used.txt
            save_used_product(product)
            
            # Optionally, sleep to avoid rate-limiting issues
            time.sleep(2)

if __name__ == "__main__":
    process_products()
