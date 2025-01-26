
import os
from PIL import Image, ImageDraw, ImageFont
from icrawler.builtin import GoogleImageCrawler

# Function to download images
def download_images(search_term, output_dir="downloaded_images", num_images=3):
    os.makedirs(output_dir, exist_ok=True)
    crawler = GoogleImageCrawler(storage={"root_dir": output_dir})
    crawler.crawl(keyword=search_term, max_num=num_images)
    print(f"Images downloaded: {os.listdir(output_dir)}")
    return [os.path.join(output_dir, img) for img in os.listdir(output_dir)]

# Function to combine images diagonally and fill a 16:9 aspect ratio
def combine_images_diagonal(image_paths, output_path, output_size=(1280, 720)):
    combined_image = Image.new("RGB", output_size, (255, 255, 255))  # Create a blank 16:9 canvas
    num_images = len(image_paths)

    for i, img_path in enumerate(image_paths):
        img = Image.open(img_path)
        img = img.resize(output_size, Image.Resampling.LANCZOS)  # Resize each image to 16:9 size

        # Calculate diagonal offset (for overlap)
        x_offset = int(i * (output_size[0] / num_images) * 0.7)  # Adjust overlap factor
        y_offset = int(i * (output_size[1] / num_images) * 0.7)
        
        # Paste the image with offsets to create a diagonal effect
        combined_image.paste(img, (-x_offset, -y_offset))

    combined_image.save(output_path)
    print(f"Combined image saved as: {output_path}")
    return output_path

# Function to add text and create a final thumbnail
def generate_thumbnail(image_path, output_path, font_path="Nature Beauty Personal Use.ttf"):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    # Define text and font
    text1 = "Best Hotel Experience"
    text2 = "Rosewood Jeddah"
    font = ImageFont.truetype(font_path, 50)  # Adjust font size if needed

    # Calculate positions for the text
    text1_width, text1_height = draw.textbbox((0, 0), text1, font=font)[2:]
    text2_width, text2_height = draw.textbbox((0, 0), text2, font=font)[2:]
    img_width, img_height = img.size

    # Position text
    text1_position = ((img_width - text1_width) // 2, img_height - text1_height - 100)
    text2_position = ((img_width - text2_width) // 2, img_height - text2_height - 50)

    # Draw text on the image
    draw.text(text1_position, text1, fill="red", font=font)
    draw.text(text2_position, text2, fill="blue", font=font)

    img.save(output_path)
    print(f"Thumbnail saved as: {output_path}")

# Main script execution
if __name__ == "__main__":
    search_term = "Rosewood Jeddah hotel booking.com"
    downloaded_images = download_images(search_term)

    combined_image = "combined_image.jpg"
    combine_images_diagonal(downloaded_images, combined_image)

    output_thumbnail = "thumbnail.jpg"
    font_file = "Nature Beauty Personal Use.ttf"  # Replace with the correct font file
    generate_thumbnail(combined_image, output_thumbnail, font_path=font_file)
