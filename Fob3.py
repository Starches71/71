

import os
from groq import Groq

# Initialize Groq client with your API key
client = Groq(api_key="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")

# Directory and file paths
AUTO_DIR = "auto"
ASK_FILE = os.path.join(AUTO_DIR, "ask.txt")
BODY_FILE = os.path.join(AUTO_DIR, "body.txt")

# Function to get product name from the ask.txt file
def get_product_name():
    try:
        with open(ASK_FILE, 'r') as file:
            product_name = file.readline().strip()  # Read the first line from ask.txt
            return product_name
    except Exception as e:
        print(f"Error reading product name from {ASK_FILE}: {e}")
        return None

# Function to query Groq API for a lazy-driven body with bullet point structure
def get_lazy_body(product_name):
    prompt = f"Give me a description and features of {product_name} with bullet point structure,each feature should be seaprsted with other with bullet point ,don't add anything in the output other than the features."

    conversation_history = [{"role": "user", "content": prompt}]
    
    try:
        # Send the prompt to Groq API
        completion = client.chat.completions.create(
            model="Llama-3.3-70b-Versatile",  # You can adjust the model as needed
            messages=conversation_history,
            temperature=0.7,  # You can tweak the temperature for creativity
            max_tokens=250,  # Adjust token length for the body
            top_p=0.9,
            stream=False,
        )
        
        # Extract and return the body
        body = completion.choices[0].message.content.strip()
        return body
    except Exception as e:
        print(f"Error while querying Groq API: {e}")
        return None

# Function to save the body to the body.txt file
def save_body_to_file(body):
    try:
        with open(BODY_FILE, 'w') as file:
            file.write(body)
        print(f"Body saved to {BODY_FILE}")
    except Exception as e:
        print(f"Error saving body to {BODY_FILE}: {e}")

# Main function to execute the process
def main():
    # Ensure the "auto" directory exists
    if not os.path.exists(AUTO_DIR):
        os.makedirs(AUTO_DIR)
    
    # Get product name from ask.txt
    product_name = get_product_name()
    
    if product_name:
        # Get lazy-driven body from Groq
        body = get_lazy_body(product_name)
        
        if body:
            # Save the body to body.txt
            save_body_to_file(body)
        else:
            print("No body generated from Groq API.")
    else:
        print("No product name found in ask.txt.")

if __name__ == "__main__":
    main()
