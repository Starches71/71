import os
from groq import Groq
import time

# Initialize Groq client with your API key
client = Groq(api_key="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")

# Directories for product names and output content
product_dir = 'prd_name'
output_dir = 'prd_content'

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to query Groq for generating a sales pitch
def query_groq(product_name):
    prompt = f"""
    Make me a sales pitch of {product_name}, 
    the title must be a short sentence that will go viral, 
    separate the title from the body with at least one line. 
    The body must be written using bullet point style, 
    and the end sentence must be short and engaging and also separated from the body with at least one line.
    """
    
    conversation_history = [{"role": "user", "content": prompt}]
    try:
        completion = client.chat.completions.create(
            model="Llama-3.3-70b-Versatile",
            messages=conversation_history,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
        )
        # Extract and return the response content
        response_content = completion.choices[0].message.content if completion.choices else "No content found"
        return response_content
    except Exception as e:
        print(f"Error while querying Groq: {e}")
        return None

# Function to process product names from the prd_name directory
def generate_sales_pitch_for_products():
    # Iterate over each product in the prd_name directory
    for product_file in os.listdir(product_dir):
        product_path = os.path.join(product_dir, product_file)
        if os.path.isfile(product_path):
            # Read the product name from the file
            with open(product_path, 'r') as f:
                product_name = f.read().strip()

            # Generate the sales pitch using the Groq API
            print(f"Generating sales pitch for: {product_name}")
            sales_pitch = query_groq(product_name)

            if sales_pitch:
                # Save the result in the prd_content directory
                output_file = os.path.join(output_dir, f"{product_file}_sales_pitch.txt")
                with open(output_file, 'w') as f:
                    f.write(sales_pitch)
                print(f"Sales pitch for {product_name} saved.")
            time.sleep(5)  # Add a small delay to prevent API overload

if __name__ == "__main__":
    generate_sales_pitch_for_products()
