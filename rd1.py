
import os

# Define the directories
TEMP_DIR = "rd"
CONTENT_DIR = "content"
OUTPUT_DIR = "output"

# Function to read the content file and extract product name and response
def read_content_file(content_file_path):
    try:
        with open(content_file_path, 'r') as file:
            return file.read().strip()  # Return content as a single string
    except Exception as e:
        print(f"Error reading content file {content_file_path}: {e}")
        return None

# Function to read the product file and check if it's 'p' or 'c'
def read_product_file(product_file_path):
    try:
        with open(product_file_path, 'r') as file:
            return file.read().strip()  # Return content as a single string (either 'p' or 'c')
    except Exception as e:
        print(f"Error reading product file {product_file_path}: {e}")
        return None

# Function to generate the sales pitch based on the product type
def generate_sales_pitch(product_name, product_type):
    if product_type == 'p':
        # Generate sales pitch for real product
        prompt = f"""
        Give me a sales pitch of {product_name}. Let the title be a short sentence that will go viral, 
        separate the title and body with at least a single line. Make the body in sales pitch in bullet point style, 
        and the end sentence should be a short sentence that will also go viral. Separate the end sentence from the body with at least one line.
        """
    elif product_type == 'c':
        # Generate sales pitch for product category
        prompt = f"""
        Make me a sales pitch of 5 best {product_name}, the title must be a short sentence that will go viral. 
        Separate the title from the body with at least one line. The body must be written using a numbered list, 
        and each product should be numbered. The end sentence must be a short sentence that will go viral and should also 
        be separated from the body with at least one line.
        """
    else:
        print(f"Invalid product type: {product_type}. Expected 'p' or 'c'.")
        return None

    return prompt

# Function to create the output directory if it doesn't exist
def create_output_directory():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory at {OUTPUT_DIR}")

# Function to save the generated prompt to a file
def save_prompt_to_file(product_name, product_type, prompt):
    # Define the filename based on the product type
    file_extension = 'outputc.txt' if product_type == 'c' else 'outputp.txt'
    file_path = os.path.join(OUTPUT_DIR, file_extension)

    try:
        with open(file_path, 'a') as file:
            file.write(f"Generated pitch for {product_name}:\n{prompt}\n")
            file.write("-" * 50 + "\n")  # Separation line
        print(f"Saved prompt for {product_name} to {file_path}")
    except Exception as e:
        print(f"Error saving prompt for {product_name}: {e}")

# Function to process the files in the content and rd directories
def process_files():
    # Create the output directory
    create_output_directory()

    # List all files in the content directory
    for content_file in os.listdir(CONTENT_DIR):
        content_file_path = os.path.join(CONTENT_DIR, content_file)

        # Read content file to get product name
        product_name = read_content_file(content_file_path)
        if not product_name:
            continue

        # Check the corresponding product file in the rd directory
        product_file_path = os.path.join(TEMP_DIR, f"{product_name}.txt")
        product_type = read_product_file(product_file_path)

        if product_type == 'p':
            print(f"Generating sales pitch for real product: {product_name}")
            pitch = generate_sales_pitch(product_name, 'p')
        elif product_type == 'c':
            print(f"Generating sales pitch for product category: {product_name}")
            pitch = generate_sales_pitch(product_name, 'c')
        else:
            print(f"Invalid product type for {product_name}. Skipping.")
            continue

        # Save the generated pitch to the output directory
        if pitch:
            save_prompt_to_file(product_name, product_type, pitch)

# Main execution
if __name__ == "__main__":
    process_files()
