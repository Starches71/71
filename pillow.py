
import os
from PIL import Image, ImageDraw, ImageFont
from icrawler.builtin import GoogleImageCrawler

# Function to download images using icrawler
def download_images(search_term, output_dir="downloaded_images", num_images=3):
    os.makedirs(output_dir, exist_ok=True)
    crawler = GoogleImageCrawler(storage={"root_dir": output_dir})
    crawler.crawl(keyword=search_term, max_num=num_images)
    print(f"Images downloaded: {os.listdir(output_dir)}")
    return [os.path.join(output_dir, img) for img in os.listdir(output_dir)]

# Function to combine images diagonally
def combine_images_diagonal(image_paths, output_path, output_size=(1024, 1024)):
    combined_image = Image.new("RGB", output_size, (255, 255, 255))
    width_offset, height_offset = 0, 0

    for img_path in image_paths:
        img = Image.open(img_path)
        img = img.resize((output_size[0] // len(image_paths), output_size[1] // len(image_paths)), Image.ANTIALIAS)
        combined_image.paste(img, (width_offset, height_offset))
        width_offset += img.width
        height_offset += img.height

    combined_image.save(output_path)
    print(f"Combined image saved as: {output_path}")
    return output_path

# Function to generate a thumbnail with text
def generate_thumbnail(image_path, output_path, font_path="Nature Beauty Personal Use.ttf"):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    # Define text and font
    text1 = "Best Hotel Experience"
    text2 = "Rosewood Jeddah"
    font = ImageFont.truetype(font_path, 40)

    # Calculate text sizes and positions
    text1_width, text1_height = draw.textbbox((0, 0), text1, font=font)[2:]
    text2_width, text2_height = draw.textbbox((0, 0), text2, font=font)[2:]
    img_width, img_height = img.size

    # Position text at the bottom-center
    text1_position = ((img_width - text1_width) // 2, img_height - text1_height - 80)
    text2_position = ((img_width - text2_width) // 2, img_height - text2_height - 40)

    # Add text to the image
    draw.text(text1_position, text1, fill="red", font=font)
    draw.text(text2_position, text2, fill="blue", font=font)

    # Save thumbnail
    img.save(output_path)
    print(f"Thumbnail saved as: {output_path}")

# Main script execution
if __name__ == "__main__":
    search_term = "Rosewood Jeddah hotel booking.com"
    downloaded_images = download_images(search_term)

    combined_image = "combined_image.jpg"
    combine_images_diagonal(downloaded_images, combined_image)

    output_thumbnail = "thumbnail.jpg"
    font_file = "Nature Beauty Personal Use.ttf"  # Replace with your font file if necessary
    generate_thumbnail(combined_image, output_thumbnail, font_path=font_file)
