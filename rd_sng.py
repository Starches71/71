
import os

# Create the directory if it doesn't exist
output_dir = 'prd_name'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read the product names from amazon.txt
with open('amazon.txt', 'r') as file:
    product_names = file.readlines()

# Clean the product names
cleaned_product_names = []

for product in product_names:
    # Remove the leading numbers and dots (e.g., "100." becomes "")
    cleaned_name = product.lstrip('0123456789.')  # remove numbers and dot from the start
    cleaned_product_names.append(cleaned_name.strip())  # Remove leading/trailing whitespace

# Save the cleaned product names into prd_name directory
output_file = os.path.join(output_dir, 'cleaned_amazon.txt')

with open(output_file, 'w') as file:
    for product in cleaned_product_names:
        file.write(product + '\n')

print(f"Cleaned product names saved to {output_file}")
