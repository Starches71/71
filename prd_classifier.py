
import requests
import os
import sys

# Constants
REPO_OWNER = "Starches71"
REPO_NAME = "71"
BRANCH = "main"
FILE_PATH = "products.txt"
RAW_URL = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{FILE_PATH}"

# GitHub Token for authentication
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_products():
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

    response = requests.get(RAW_URL, headers=headers)

    if response.status_code == 200:
        with open(FILE_PATH, "w") as f:
            f.write(response.text)
        print("✅ Successfully fetched products.txt")
    else:
        print(f"❌ Failed to fetch products.txt: {response.status_code}")
        sys.exit(1)

def process_products(limit=50):
    if not os.path.exists(FILE_PATH):
        print("❌ products.txt not found after fetch.")
        sys.exit(1)

    with open(FILE_PATH, "r") as f:
        products = [line.strip() for line in f.readlines() if line.strip()]

    if not products:
        print("⚠️ No products to process.")
        sys.exit(0)

    # Process only the specified number of products
    products_to_process = products[:limit]
    
    for idx, product in enumerate(products_to_process, 1):
        print(f"🔹 Processing {idx}/{limit}: {product}")

    print("✅ Done processing.")

if __name__ == "__main__":
    fetch_products()
    process_products(limit=50)
