
import os
from groq import Groq

# Initialize Groq client with your API key
client = Groq(api_key="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")

# Directory and file paths
AUTO_DIR = "auto"
ASK_FILE = os.path.join(AUTO_DIR, "ask.txt")
TITTLE_FILE = os.path.join(AUTO_DIR, "tittle.txt")

# Function to get product name from the ask.txt file
def get_product_name():
    try:
        with open(ASK_FILE, 'r') as file:
            product_name = file.readline().strip()  # Read the first line from ask.txt
            return product_name
    except Exception as e:
        print(f"Error reading product name from {ASK_FILE}: {e}")
        return None

# Function to query Groq API for a lazy-driven headline
def get_lazy_headline(product_name):
    prompt = f"Give me a lazy driven headline of {product_name} plz just output the headline only, don't add anything else in the output."

    conversation_history = [{"role": "user", "content": prompt}]
    
    try:
        # Send the prompt to Groq API
        completion = client.chat.completions.create(
            model="Llama-3.3-70b-Versatile",  # You can adjust the model as needed
            messages=conversation_history,
            temperature=0.7,  # You can tweak the temperature for creativity
            max_tokens=100,
            top_p=0.9,
            stream=False,
        )
        
        # Extract and return the headline
        headline = completion.choices[0].message.content.strip()
        return headline
    except Exception as e:
        print(f"Error while querying Groq API: {e}")
        return None

# Function to save the headline to the tittle.txt file
def save_headline_to_file(headline):
    try:
        with open(TITTLE_FILE, 'w') as file:
            file.write(headline)
        print(f"Headline saved to {TITTLE_FILE}")
    except Exception as e:
        print(f"Error saving headline to {TITTLE_FILE}: {e}")

# Main function to execute the process
def main():
    # Ensure the "auto" directory exists
    if not os.path.exists(AUTO_DIR):
        os.makedirs(AUTO_DIR)
    
    # Get product name from ask.txt
    product_name = get_product_name()
    
    if product_name:
        # Get lazy-driven headline from Groq
        headline = get_lazy_headline(product_name)
        
        if headline:
            # Save the headline to tittle.txt
            save_headline_to_file(headline)
        else:
            print("No headline generated from Groq API.")
    else:
        print("No product name found in ask.txt.")

if __name__ == "__main__":
    main()
