
import os

# Create the directory if it doesn't exist
output_dir = 'prd_name'
os.makedirs(output_dir, exist_ok=True)

# Read only the first product name from amazon.txt
with open('amazon.txt', 'r') as file:
    first_product = file.readline().lstrip('0123456789.').strip()  # Read first line, remove numbers/dots, and strip spaces

# Save the first product name in a separate file
if first_product:  # Ensure it's not empty
    output_file = os.path.join(output_dir, 'product.txt')
    
    with open(output_file, 'w') as file:
        file.write(first_product + '\n')

    print(f"Saved: {output_file}")
else:
    print("Error: amazon.txt is empty.")
