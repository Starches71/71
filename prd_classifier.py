
import os
import requests
import base64
import time
from groq import Groq

# GitHub Credentials
GITHUB_TOKEN = "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"
REPO_OWNER = "Starches71"
REPO_NAME = "71"

# GitHub File Paths
PRODUCTS_FILE = "products.txt"
P_FILE = "p.txt"
C_FILE = "c.txt"

# Groq API Key
client = Groq(api_key="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")

def fetch_file_content(file_path):
    """Fetch file content from GitHub."""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        file_data = response.json()
        content = base64.b64decode(file_data['content']).decode()
        return content.splitlines(), file_data['sha']
    else:
        print(f"Failed to fetch {file_path}: {response.status_code}")
        return [], None

def update_file(file_path, new_content, sha):
    """Update file in GitHub with new content."""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    encoded_content = base64.b64encode(new_content.encode()).decode()
    data = {
        "message": f"Update {file_path}",
        "content": encoded_content,
        "sha": sha
    }
    
    response = requests.put(url, json=data, headers=headers)
    if response.status_code == 200:
        print(f"{file_path} updated successfully.")
    else:
        print(f"Failed to update {file_path}: {response.status_code}")

def query_llm(product):
    """Ask Groq LLM if the product is a real product (p) or category (c)."""
    prompt = f"Is the {product} a real product on Amazon or just a product category? Answer 'p' if it's a product, and answer 'c' if it's a product category. Just answer 'p' or 'c' only."
    conversation_history = [{"role": "user", "content": prompt}]
    
    try:
        completion = client.chat.completions.create(
            model="Llama-3.3-70b-Versatile",
            messages=conversation_history,
            temperature=0,
            max_tokens=10,
            top_p=0,
            stream=False,
        )
        response_content = completion.choices[0].message.content if completion.choices else "No content found"
        return response_content.strip().lower()
    except Exception as e:
        print(f"Error querying LLM: {e}")
        return None

def process_product():
    # Fetch products.txt
    products, products_sha = fetch_file_content(PRODUCTS_FILE)
    if not products:
        print("No products to process.")
        return

    product = products[0]
    print(f"Processing: {product}")

    # Query Groq LLM
    response = None
    while response not in ['p', 'c']:
        response = query_llm(product)
        if response not in ['p', 'c']:
            print(f"Invalid response '{response}', retrying...")
            time.sleep(2)

    print(f"LLM Response: {response}")

    # Fetch & update the correct file
    target_file = P_FILE if response == 'p' else C_FILE
    existing_content, target_sha = fetch_file_content(target_file)
    
    new_content = "\n".join(existing_content + [product])
    update_file(target_file, new_content, target_sha)

    # Remove processed product from products.txt
    products.pop(0)
    update_file(PRODUCTS_FILE, "\n".join(products), products_sha)

if __name__ == "__main__":
    process_product()
