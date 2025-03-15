
import os
import requests
from groq import Groq
import base64

# Initialize Groq client
client = Groq(api_key="your_groq_api_key")

# GitHub details
GITHUB_TOKEN = "your_github_token"
REPO_OWNER = "Starches71"
REPO_NAME = "71"
BRANCH = "main"

# Define directories and file paths
AUTO_DIR = "auto"
PRODUCT_FILE = os.path.join(AUTO_DIR, "product.txt")
ASK_FILE = os.path.join(AUTO_DIR, "ask.txt")
NO_FILE = os.path.join(AUTO_DIR, "auto_no.txt")

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

# Save the invalid product to auto_no.txt in the GitHub repository
def save_to_auto_no(product_name):
    file_path = "auto_no.txt"
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    # Fetch the current file to get its SHA
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        file_data = response.json()
        file_sha = file_data['sha']
        current_content = base64.b64decode(file_data['content']).decode()

        # Append the new product
        new_content = current_content + f"\n{product_name}"
        encoded_content = base64.b64encode(new_content.encode()).decode()

        # Update GitHub file
        data = {"message": "Added new product to auto_no.txt", "content": encoded_content, "sha": file_sha}
        update_response = requests.put(url, json=data, headers=headers)

        if update_response.status_code == 200:
            print(f"Product '{product_name}' saved to auto_no.txt in GitHub.")
        else:
            print(f"Failed to update auto_no.txt: {update_response.status_code} - {update_response.text}")
    else:
        print("auto_no.txt not found, creating a new file...")
        encoded_content = base64.b64encode(f"{product_name}\n".encode()).decode()
        data = {"message": "Create auto_no.txt", "content": encoded_content}
        create_response = requests.put(url, json=data, headers=headers)

        if create_response.status_code == 201:
            print(f"Created auto_no.txt and added '{product_name}'.")
        else:
            print(f"Failed to create auto_no.txt: {create_response.status_code} - {create_response.text}")

# Trigger GitHub Actions to replace product.txt from auto.txt
def trigger_github_action():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/update_product.yml/dispatches"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
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
