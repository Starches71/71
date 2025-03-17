import os
from groq import Groq

# Load API key securely from environment variable
GROQ_API_KEY = os.getenv("GROQ_API")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API key is missing. Please set it as an environment variable.")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Directory and file paths
AUTO_DIR = "auto"
ASK_FILE = os.path.join(AUTO_DIR, "ask.txt")
TITLE_FILE = os.path.join(AUTO_DIR, "title.txt")  # Correct file path for title.txt

# Ensure the auto directory exists
if not os.path.exists(AUTO_DIR):
    os.makedirs(AUTO_DIR)

# Function to get product name from ask.txt
def get_product_name():
    try:
        if not os.path.exists(ASK_FILE):
            print(f"Warning: {ASK_FILE} does not exist.")
            return None
        
        with open(ASK_FILE, 'r') as file:
            product_name = file.readline().strip()
            if not product_name:
                print(f"Warning: {ASK_FILE} is empty.")
                return None
            return product_name
    except Exception as e:
        print(f"Error reading product name from {ASK_FILE}: {e}")
        return None

# Function to query Groq API
def query_groq(prompt):
    conversation_history = [{"role": "user", "content": prompt}]
    
    try:
        print(f"Querying Groq API with prompt: {prompt}")
        completion = client.chat.completions.create(
            model="Llama-3.3-70b-Versatile",
            messages=conversation_history,
            temperature=0.7,
            max_tokens=100,
            top_p=0.9,
            stream=False,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error while querying Groq API: {e}")
        return None

# Function to generate headline
def generate_headline(product_name):
    category_prompt = f"What is the product category of {product_name}? Just output the category name, nothing else."
    product_category = query_groq(category_prompt)

    task_prompt = f"What task does {product_name} automate? Just output the task, nothing else."
    automation_task = query_groq(task_prompt)

    if product_category and automation_task:
        return f"This {product_category} can do {automation_task} for you."
    return None

# Function to save headline
def save_headline_to_file(headline):
    try:
        with open(TITLE_FILE, 'w') as file:
            file.write(headline)
        print(f"Headline saved to {TITLE_FILE}")
    except Exception as e:
        print(f"Error saving headline to {TITLE_FILE}: {e}")

# Main function
def main():
    # Ensure the auto directory exists
    if not os.path.exists(AUTO_DIR):
        os.makedirs(AUTO_DIR)
    
    product_name = get_product_name()
    
    if product_name:
        headline = generate_headline(product_name)
        
        if headline:
            save_headline_to_file(headline)
        else:
            print("Failed to generate headline.")
    else:
        print("No product name found in ask.txt.")

if __name__ == "__main__":
    main()
