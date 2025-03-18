import os
from icrawler.builtin import GoogleImageCrawler
from PIL import Image

# Step 1: Download 3 images
def download_images(search_term, output_dir="downloaded_images", num_images=3):
    os.makedirs(output_dir, exist_ok=True)
    crawler = GoogleImageCrawler(storage={"root_dir": output_dir})
    crawler.crawl(keyword=search_term, max_num=num_images)
    downloaded_files = [os.path.join(output_dir, f"{str(i+1).zfill(6)}.jpg") for i in range(num_images)]
    print("Images downloaded:", downloaded_files)
    return downloaded_files

# Step 2: Crop and Combine images in a V-like diagonal layout
def combine_images_v_like(images, output_image="combined_image.jpg", final_width=1280, final_height=720):
    # Open images
    img1 = Image.open(images[0])
    img2 = Image.open(images[1])
    img3 = Image.open(images[2])

    # Define the target width and height (16:9 aspect ratio)
    target_width = final_width
    target_height = final_height
    
    # Resize images to fit within the target size (cropping the middle section)
    img1 = img1.resize((target_width // 3, target_height))
    img2 = img2.resize((target_width // 3, target_height))
    img3 = img3.resize((target_width // 3, target_height))

    # Crop images to focus on the center (creating the "V" effect)
    img1 = img1.crop((img1.width // 4, 0, img1.width * 3 // 4, img1.height))
    img2 = img2.crop((img2.width // 4, 0, img2.width * 3 // 4, img2.height))
    img3 = img3.crop((img3.width // 4, 0, img3.width * 3 // 4, img3.height))

    # Create a new blank image for the V-like layout
    combined_img = Image.new("RGB", (target_width, target_height), (255, 255, 255))

    # Place images in the V-like diagonal layout
    # Image 1: Left side
    combined_img.paste(img1, (0, target_height // 2))  # Left side of the "V"
    
    # Image 2: Center part, slightly lower than image 1
    combined_img.paste(img2, (target_width // 3, 0))  # Center of the "V"
    
    # Image 3: Right side, overlap with image 2
    combined_img.paste(img3, (target_width * 2 // 3, target_height // 2))  # Right side of the "V"

    # Save the combined image
    combined_img.save(output_image)
    print("Combined image saved as:", output_image)
    return output_image

# Step 3: Generate a thumbnail with text and thick black borders
def generate_thumbnail(input_image, output_image, font_path="Nature Beauty Personal Use.ttf"):
    # Check if the input image exists
    if not os.path.exists(input_image):
        print("Input image not found! Aborting thumbnail generation.")
        return

    # Check if the font exists
    if not os.path.exists(font_path):
        print("Font file not found! Please provide a valid path to the font.")
        return

    # FFmpeg command to apply text, shadow, and vignette with thicker black borders
    ffmpeg_command = (
        f'ffmpeg -y -i "{input_image}" '
        f'-vf "format=yuv420p,'
        f'curves=preset=lighter,'
        f'drawtext=text=\'Best Hotels\':'
        f'fontfile=\'{font_path}\':'
        f'fontcolor=white:fontsize=150:borderw=8:bordercolor=black:'  # Thicker border with borderw=8
        f'x=(w-text_w)/2:y=(h-text_h)/2-100,'
        f'drawtext=text=\'Jeddah\':'
        f'fontfile=\'{font_path}\':'
        f'fontcolor=white:fontsize=150:borderw=8:bordercolor=black:'  # Thicker border with borderw=8
        f'x=(w-text_w)/2:y=(h-text_h)/2+100,'
        f'vignette=PI/4" '
        f'"{output_image}"'
    )

    print("Running FFmpeg command:", ffmpeg_command)
    result = os.system(ffmpeg_command)
    if result == 0:
        print("Thumbnail generated successfully:", output_image)
    else:
        print("Failed to generate thumbnail.")

if __name__ == "__main__":
    # Step 1: Download 3 images
    search_query = "Rosewood Jeddah hotel booking.com"
    downloaded_images = download_images(search_query)

    # Step 2: Combine the images in a V-like diagonal layout
    combined_image = "combined_image.jpg"
    combine_images_v_like(downloaded_images, combined_image)

    # Step 3: Generate thumbnail with text and thicker black borders
    font_file = "Nature Beauty Personal Use.ttf"  # Font file in the main branch
    output_thumbnail = "thumbnail_with_text_border.jpg"
    generate_thumbnail(combined_image, output_thumbnail, font_path=font_file)
