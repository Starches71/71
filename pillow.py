
from PIL import Image, ImageDraw, ImageFont
import os
from icrawler.builtin import GoogleImageCrawler

# Step 1: Download images
def download_images(search_term, output_dir="downloaded_images", num_images=3):
    os.makedirs(output_dir, exist_ok=True)
    crawler = GoogleImageCrawler(storage={"root_dir": output_dir})
    crawler.crawl(keyword=search_term, max_num=num_images)
    downloaded_files = [os.path.join(output_dir, f"{str(i+1).zfill(6)}.jpg") for i in range(num_images)]
    print("Images downloaded:", downloaded_files)
    return downloaded_files

# Step 2: Combine images diagonally into a 16:9 thumbnail
def combine_images_diagonal(images, output_image="combined_image.jpg", output_size=(1280, 720)):
    # Open the images and resize them to 16:9 segments
    cropped_images = []
    for img_path in images:
        img = Image.open(img_path)
        img = img.resize((output_size[0] // 3, output_size[1]), Image.ANTIALIAS)  # Resize each image to 1/3 width
        cropped_images.append(img)

    # Create a blank canvas for the combined image
    combined_image = Image.new("RGB", output_size)

    # Paste the images diagonally
    for i, img in enumerate(cropped_images):
        x_offset = i * (output_size[0] // 3)
        combined_image.paste(img, (x_offset, 0))

    # Save the combined image
    combined_image.save(output_image)
    print(f"Combined image saved as: {output_image}")
    return output_image

# Step 3: Add text with thick black borders
def add_text_with_border(input_image, output_image, text="Best Hotels in Jeddah", font_path="Nature Beauty Personal Use.ttf"):
    # Open the combined image
    img = Image.open(input_image)
    draw = ImageDraw.Draw(img)

    # Load font (adjust font size as needed)
    try:
        font = ImageFont.truetype(font_path, 80)
    except IOError:
        print("Font file not found! Please provide a valid path.")
        return

    # Text position
    text_width, text_height = draw.textsize(text, font=font)
    x = (img.width - text_width) // 2
    y = (img.height - text_height) // 2

    # Draw black border (by drawing multiple layers of text slightly offset)
    border_thickness = 5
    for offset_x in range(-border_thickness, border_thickness + 1):
        for offset_y in range(-border_thickness, border_thickness + 1):
            draw.text((x + offset_x, y + offset_y), text, font=font, fill="black")

    # Draw white text on top
    draw.text((x, y), text, font=font, fill="white")

    # Save the final thumbnail
    img.save(output_image)
    print(f"Thumbnail with text saved as: {output_image}")

# Main function
if __name__ == "__main__":
    # Step 1: Download images
    search_query = "Rosewood Jeddah hotel booking.com"
    downloaded_images = download_images(search_query)

    # Step 2: Combine images
    combined_image = "combined_image.jpg"
    combine_images_diagonal(downloaded_images, combined_image)

    # Step 3: Add text with thick borders
    font_file = "Nature Beauty Personal Use.ttf"  # Ensure the font file exists in your working directory
    output_thumbnail = "thumbnail_with_text_border.jpg"
    add_text_with_border(combined_image, output_thumbnail, font_path=font_file)
