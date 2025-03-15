
import os
from groq import Groq

# Initialize Groq client with your API key
client = Groq(api_key="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")

# Directory and file paths
AUTO_DIR = "auto"
ASK_FILE = os.path.join(AUTO_DIR, "ask.txt")
HASHTAG_FILE = os.path.join(AUTO_DIR, "hashtag.txt")

# Function to get product name from the ask.txt file
def get_product_name():
    try:
        with open(ASK_FILE, 'r') as file:
            product_name = file.readline().strip()  # Read the first line from ask.txt
            return product_name
    except Exception as e:
        print(f"Error reading product name from {ASK_FILE}: {e}")
        return None

# Function to query Groq API for hashtags
def get_hashtags(product_name):
    prompt = f"Give me hashtags for {product_name}, please output hashtags only don't output anything else."

    conversation_history = [{"role": "user", "content": prompt}]
    
    try:
        # Send the prompt to Groq API
        completion = client.chat.completions.create(
            model="Llama-3.3-70b-Versatile",  # You can adjust the model as needed
            messages=conversation_history,
            temperature=0.7,  # You can tweak the temperature for creativity
            max_tokens=250,  # Adjust token length for hashtags
            top_p=0.9,
            stream=False,
        )
        
        # Extract and return hashtags
        hashtags = completion.choices[0].message.content.strip()
        return hashtags
    except Exception as e:
        print(f"Error while querying Groq API: {e}")
        return None

# Function to save the hashtags to the hashtag.txt file
def save_hashtags_to_file(hashtags):
    try:
        with open(HASHTAG_FILE, 'w') as file:
            file.write(hashtags)
        print(f"Hashtags saved to {HASHTAG_FILE}")
    except Exception as e:
        print(f"Error saving hashtags to {HASHTAG_FILE}: {e}")

# Main function to execute the process
def main():
    # Ensure the "auto" directory exists
    if not os.path.exists(AUTO_DIR):
        os.makedirs(AUTO_DIR)
    
    # Get product name from ask.txt
    product_name = get_product_name()
    
    if product_name:
        # Get hashtags from Groq
        hashtags = get_hashtags(product_name)
        
        if hashtags:
            # Save the hashtags to hashtag.txt
            save_hashtags_to_file(hashtags)
        else:
            print("No hashtags generated from Groq API.")
    else:
        print("No product name found in ask.txt.")

if __name__ == "__main__":
    main()
