
import os
from icrawler.builtin import GoogleImageCrawler

# Step 1: Download an image using iCrawler
def download_image(query, output_dir, max_num=1):
    os.makedirs(output_dir, exist_ok=True)
    google_crawler = GoogleImageCrawler(storage={'root_dir': output_dir})
    google_crawler.crawl(keyword=query, max_num=max_num)
    image_path = os.path.join(output_dir, "000001.jpg")
    return image_path

# Step 2: Generate a thumbnail with text using FFmpeg
def generate_thumbnail_with_text(input_image, output_image, text, font="DejaVuSans-Bold", font_size=36, color="white"):
    if not os.path.exists(input_image):
        print(f"Input image does not exist: {input_image}")
        return

    # FFmpeg command to overlay text on the image
    command = [
        "ffmpeg",
        "-i", input_image,
        "-vf", f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/{font}.ttf:text='{text}':fontcolor={color}:fontsize={font_size}:x=(w-text_w)/2:y=(h-text_h)-50",
        "-y", output_image
    ]

    # Run the FFmpeg command
    result = os.system(" ".join(command))
    if result == 0:
        print(f"Thumbnail generated: {output_image}")
    else:
        print("Failed to generate thumbnail.")

# Main script
if __name__ == "__main__":
    query = "San Francisco cityscape"
    output_dir = "downloaded_images"
    output_image = "thumbnail_with_text.jpg"
    text = "Welcome to San Francisco!"

    # Step 1: Download the image
    input_image = download_image(query, output_dir)

    # Step 2: Generate the thumbnail with text
    generate_thumbnail_with_text(input_image, output_image, text)
