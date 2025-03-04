
import requests
import os
import sys
from git import Repo

# Constants
REPO_OWNER = "Starches71"
REPO_NAME = "71"
BRANCH = "main"
FILE_PATH = "products.txt"
RAW_URL = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{FILE_PATH}"

# API Keys & URLs
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/classify"

# File Paths
C_FILE = "c.txt"
P_FILE = "p.txt"

def fetch_products():
    """Fetches products.txt from GitHub"""
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"} if GROQ_API_KEY else {}

    response = requests.get(RAW_URL, headers=headers)

    if response.status_code == 200:
        with open(FILE_PATH, "w") as f:
            f.write(response.text)
        print("✅ Successfully fetched products.txt")
    else:
        print(f"❌ Failed to fetch products.txt: {response.status_code}")
        sys.exit(1)

def classify_product(product):
    """Uses Groq API to classify the product as 'C' or 'P'"""
    if not GROQ_API_KEY:
        print("❌ Missing GROQ_API_KEY. Cannot classify products.")
        sys.exit(1)

    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {"text": product}

    response = requests.post(GROQ_URL, headers=headers, json=data)

    if response.status_code == 200:
        category = response.json().get("category", "").upper()
        return category if category in ["C", "P"] else None

    print(f"⚠️ Failed to classify '{product}', skipping.")
    return None

def commit_and_push_changes():
    """Commit and push the changes to GitHub using GitHub Actions Token"""
    try:
        repo = Repo(".")
        # Stage changes
        repo.git.add([C_FILE, P_FILE])

        # Commit the changes
        repo.index.commit("Classified products and updated c.txt and p.txt")

        # Push the changes to GitHub
        origin = repo.remote(name='origin')
        origin.push()
        print("✅ Successfully pushed changes to GitHub.")
    except Exception as e:
        print(f"❌ Failed to push changes: {e}")
        sys.exit(1)

def process_products(limit=50):
    """Processes up to `limit` products and saves them in c.txt or p.txt"""
    if not os.path.exists(FILE_PATH):
        print("❌ products.txt not found after fetch.")
        sys.exit(1)

    with open(FILE_PATH, "r") as f:
        products = [line.strip() for line in f.readlines() if line.strip()]

    if not products:
        print("⚠️ No products to process.")
        sys.exit(0)

    products_to_process = products[:limit]
    c_products, p_products = [], []

    for idx, product in enumerate(products_to_process, 1):
        category = classify_product(product)

        if category == "C":
            c_products.append(product)
        elif category == "P":
            p_products.append(product)

        print(f"🔹 {idx}/{limit}: {product} → {category or 'UNKNOWN'}")

    # Save to files
    if c_products:
        with open(C_FILE, "w") as f:
            f.write("\n".join(c_products))
        print(f"✅ Saved {len(c_products)} 'C' products to {C_FILE}")

    if p_products:
        with open(P_FILE, "w") as f:
            f.write("\n".join(p_products))
        print(f"✅ Saved {len(p_products)} 'P' products to {P_FILE}")

    print("✅ Done processing.")

    # Commit and push the changes to the repo
    commit_and_push_changes()

if __name__ == "__main__":
    fetch_products()
    process_products(limit=50)
