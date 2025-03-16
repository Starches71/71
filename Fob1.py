import os
from groq import Groq

# Initialize Groq client with your API key
client = Groq(api_key="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")

# Directory and file paths
AUTO_DIR = "auto"
ASK_FILE = os.path.join(AUTO_DIR, "ask.txt")
TITTLE_FILE = os.path.join(AUTO_DIR, "tittle.txt")

# Function to get product name from ask.txt file
def get_product_name():
    try:
        with open(ASK_FILE, 'r') as file:
            product_name = file.readline().strip()  # Read the first line
            return product_name
    except Exception as e:
        print(f"Error reading product name from {ASK_FILE}: {e}")
        return None

# Function to query Groq API
def query_groq(prompt):
    conversation_history = [{"role": "user", "content": prompt}]
    
    try:
        # Send request to Groq API
        completion = client.chat.completions.create(
            model="Llama-3.3-70b-Versatile",  # Adjust model as needed
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
    # API call 1: Get product category
    category_prompt = f"What is the product category of {product_name}? Just output the category name, nothing else."
    product_category = query_groq(category_prompt)

    # API call 2: Get automation task
    task_prompt = f"What task does {product_name} automate? Just output the task, nothing else."
    automation_task = query_groq(task_prompt)

    if product_category and automation_task:
        return f"This {product_category} can do {automation_task} for you."
    else:
        return None

# Function to save headline
def save_headline_to_file(headline):
    try:
        with open(TITTLE_FILE, 'w') as file:
            file.write(headline)
        print(f"Headline saved to {TITTLE_FILE}")
    except Exception as e:
        print(f"Error saving headline to {TITTLE_FILE}: {e}")

# Main function
def main():
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
