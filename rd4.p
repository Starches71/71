import os

# Paths to directories
output_dir = "output"
aff_dir = "aff"
images_dir = "images"
post_dir = "post"

# Function to create the post for outputp.txt
def create_post_outputp():
    with open(os.path.join(output_dir, "outputp.txt"), 'r') as f:
        content = f.read()
    
    # Get the affiliate link (we assume only 1 link in outputp.txt)
    with open(os.path.join(aff_dir, "1.aff"), 'r') as f:
        aff_link = f.read().strip()
    
    # Collect images
    images = []
    for i in range(1, 8):  # Assuming 7 images are needed
        image_path = os.path.join(images_dir, f"{i}.png")
        if os.path.exists(image_path):
            images.append(f"![Image {i}]({image_path})")
    
    # Combine everything
    post_content = f"# {content.splitlines()[0]}\n\n"  # Title is the first line of content
    post_content += f"{content}\n\n"  # Body
    post_content += f"## Affiliate Link:\n{aff_link}\n\n"  # Affiliate link
    post_content += f"## Images:\n" + "\n".join(images)  # Images
    
    # Save the post to the post directory
    post_file = os.path.join(post_dir, "post_outputp.txt")
    with open(post_file, 'w') as f:
        f.write(post_content)
    print(f"Post saved as {post_file}")

# Function to create the post for outputc.txt
def create_post_outputc():
    with open(os.path.join(output_dir, "outputc.txt"), 'r') as f:
        content = f.read().splitlines()
    
    # Process each product in outputc.txt
    post_content = "# Best Products for 2025\n\n"
    for i in range(1, 6):  # Assuming 5 products in outputc.txt
        product_line = content[i-1]
        product_name = product_line.split('.')[1].split('.')[0]  # Get product name before first full stop
        
        # Read the corresponding affiliate link and images
        with open(os.path.join(aff_dir, f"{i}.aff"), 'r') as f:
            aff_link = f.read().strip()
        
        images = []
        for j in range(1, 6):  # Assuming 5 images per product
            image_path = os.path.join(images_dir, f"{i}_{j}.png")
            if os.path.exists(image_path):
                images.append(f"![Image {i}_{j}]({image_path})")
        
        # Add product content to the post
        post_content += f"## {i}. {product_name}\n\n{product_line}\n\n"
        post_content += f"### Affiliate Link:\n{aff_link}\n\n"
        post_content += f"### Images:\n" + "\n".join(images) + "\n\n"
    
    # Conclusion section
    post_content += "## Conclusion:\nThis is a list of the top 5 products for 2025. Choose the one that best suits your needs!"
    
    # Save the post to the post directory
    post_file = os.path.join(post_dir, "post_outputc.txt")
    with open(post_file, 'w') as f:
        f.write(post_content)
    print(f"Post saved as {post_file}")

# Main function to decide whether to process outputp.txt or outputc.txt
def main():
    # Check if outputp.txt exists in the output directory
    if os.path.exists(os.path.join(output_dir, "outputp.txt")):
        create_post_outputp()
    
    # Check if outputc.txt exists in the output directory
    elif os.path.exists(os.path.join(output_dir, "outputc.txt")):
        create_post_outputc()
    else:
        print("Neither outputp.txt nor outputc.txt found in the output directory.")

if __name__ == "__main__":
    main()
