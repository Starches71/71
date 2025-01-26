
import os
from PIL import Image, ImageDraw, ImageFont
from icrawler.builtin import GoogleImageCrawler

# Step 1: Download 3 images using icrawler
def download_images(search_term, output_dir="downloaded_images", num_images=3):
    os.makedirs(output_dir, exist_ok=True)
    crawler = GoogleImageCrawler(storage={"root_dir": output_dir})
    crawler.crawl(keyword=search_term, max_num=num_images)
    downloaded_files = [os.path.join(output_dir, f"{str(i+1).zfill(6)}.jpg") for i in range(num_images)]
    print("Images downloaded:", downloaded_files)
    return downloaded_files

# Step 2: Combine images diagonally
def combine_images_diagonal(images, output_image="combined_image.jpg", output_size=(1280, 720)):
    # Create a blank canvas with the specified output size
    canvas = Image.new("RGB", output_size, (255, 255, 255))

    for i, image_path in enumerate(images):
        img = Image.open(image_path)

        # Resize each image to fit 1/3 of the canvas width while maintaining the height
        img = img.resize((output_size[0] // 3, output_size[1]), Image.Resampling.LANCZOS)  # Updated resizing method
        x_offset = (output_size[0] // 3) * i  # Position for each image

        # Paste the image diagonally
        canvas.paste(img, (x_offset, 0))

    canvas.save(output_image)
    print(f"Combined image saved as: {output_image}")
    return output_image

# Step 3: Add text to the combined image
def generate_thumbnail(input_image, output_image, font_path="Nature Beauty Personal Use.ttf"):
    # Check if the input image exists
    if not os.path.exists(input_image):
        print("Input image not found! Aborting thumbnail generation.")
        return

    # Check if the font exists
    if not os.path.exists(font_path):
        print("Font file not found! Please provide a valid path to the font.")
        return

    # Open the combined image
    img = Image.open(input_image)
    draw = ImageDraw.Draw(img)

    # Add text in the center with thick black borders
    font_size = 80
    font = ImageFont.truetype(font_path, font_size)

    # First text
    text1 = "Best Hotels"
    text1_width, text1_height = draw.textsize(text1, font=font)
    x1 = (img.width - text1_width) // 2
    y1 = (img.height - text1_height) // 2 - 50
    draw.text((x1 - 2, y1 - 2), text1, font=font, fill="black")
    draw.text((x1 + 2, y1 - 2), text1, font=font, fill="black")
    draw.text((x1 + 2, y1 + 2), text1, font=font, fill="black")
    draw.text((x1 - 2, y1 + 2), text1, font=font, fill="black")
    draw.text((x1, y1), text1, font=font, fill="white")

    # Second text
    text2 = "Jeddah"
    text2_width, text2_height = draw.textsize(text2, font=font)
    x2 = (img.width - text2_width) // 2
    y2 = (img.height - text2_height) // 2 + 50
    draw.text((x2 - 2, y2 - 2), text2, font=font, fill="black")
    draw.text((x2 + 2, y2 - 2), text2, font=font, fill="black")
    draw.text((x2 + 2, y2 + 2), text2, font=font, fill="black")
    draw.text((x2 - 2, y2 + 2), text2, font=font, fill="black")
    draw.text((x2, y2), text2, font=font, fill="white")

    # Save the final thumbnail
    img.save(output_image)
    print(f"Thumbnail generated successfully: {output_image}")

if __name__ == "__main__":
    # Step 1: Download 3 images
    search_query = "Rosewood Jeddah hotel booking.com"
    downloaded_images = download_images(search_query)

    # Step 2: Combine the images diagonally
    combined_image = "combined_image.jpg"
    combine_images_diagonal(downloaded_images, combined_image)

    # Step 3: Generate thumbnail with text and thicker black borders
    font_file = "Nature Beauty Personal Use.ttf"  # Font file in the main branch
    output_thumbnail = "thumbnail_with_text_border.jpg"
    generate_thumbnail(combined_image, output_thumbnail, font_path=font_file)
