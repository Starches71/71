import os
import requests
from groq import Groq
import base64

# Initialize Groq client with hardcoded API key
client = Groq(api_key="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")

# GitHub details
REPO_OWNER = "Starches71"
REPO_NAME = "71"
BRANCH = "main"

# Define directories and file paths
AUTO_DIR = "auto"
PRODUCT_FILE = os.path.join(AUTO_DIR, "product.txt")
ASK_FILE = os.path.join(AUTO_DIR, "ask.txt")
NO_FILE = "auto_no.txt"  # Now stored directly in the main repo

# Ensure auto directory exists
os.makedirs(AUTO_DIR, exist_ok=True)

# Function to read the product name from product.txt
def load_product():
    if os.path.exists(PRODUCT_FILE):
        with open(PRODUCT_FILE, "r") as file:
            product_name = file.readline().strip()
        return product_name if product_name else None
    return None

# Query Groq to check if the product exists on Amazon
def query_groq(product_name):
    prompt = f"Do you know a product on Amazon called {product_name}? If yes, type yes. If no, type no. Only type yes or no only."

    try:
        response = client.chat.completions.create(
            model="Llama-3.3-70b-Versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=5
        )
        reply = response.choices[0].message.content.strip().lower()
        return reply
    except Exception as e:
        print(f"Error querying Groq: {e}")
        return None

# Save the product to ask.txt if valid
def save_to_ask_file(product_name):
    with open(ASK_FILE, "a") as file:
        file.write(f"{product_name}\n")
    print(f"Saved '{product_name}' to ask.txt.")

# Save the invalid product to auto_no.txt in the main repo
def save_to_auto_no(product_name):
    with open(NO_FILE, "a") as file:
        file.write(f"{product_name}\n")
    print(f"Saved '{product_name}' to auto_no.txt.")

# Trigger GitHub Actions to replace product.txt from auto.txt
def trigger_github_action():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/update_product.yml/dispatches"
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"ref": BRANCH}

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 204:
        print("Triggered GitHub Actions to update product.txt.")
    else:
        print(f"Failed to trigger GitHub Actions: {response.status_code} - {response.text}")

# Main function
def process_product():
    product_name = load_product()
    if not product_name:
        print("No product found in product.txt.")
        return

    print(f"Checking product: {product_name}")
    response = query_groq(product_name)

    if response == "yes":
        save_to_ask_file(product_name)
    elif response == "no":
        save_to_auto_no(product_name)
        trigger_github_action()  # Replace product.txt with a new one
    else:
        print(f"Unexpected response: {response}")

# Run the script
if __name__ == "__main__":
    process_product()
