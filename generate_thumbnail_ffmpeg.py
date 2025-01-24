
import os
from icrawler.builtin import GoogleImageCrawler

def download_image(query, save_dir="downloaded_images", max_images=1):
    """
    Downloads images from Google based on a search query.
    
    Parameters:
    - query (str): The search query for the images.
    - save_dir (str): Directory to save the downloaded images.
    - max_images (int): Maximum number of images to download.
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    crawler = GoogleImageCrawler(storage={"root_dir": save_dir})
    crawler.crawl(keyword=query, max_num=max_images)
    print(f"Image downloaded as: {save_dir}/000001.jpg")


def generate_thumbnail(input_image="downloaded_images/000001.jpg", 
                       output_image="thumbnail_with_text.jpg", 
                       text="best hotels\n       in\n     jeddah", 
                       font_path="Nature Beauty Personal Use.ttf"):
    """
    Generates a thumbnail image with text overlay using FFmpeg.

    Parameters:
    - input_image (str): Path to the input image.
    - output_image (str): Path to save the output thumbnail.
    - text (str): Text to overlay on the image.
    - font_path (str): Path to the .ttf font file.
    """
    # Get the absolute path of the font file
    absolute_font_path = os.path.abspath(font_path)
    
    # Debugging statements
    print("Using font file at:", absolute_font_path)
    print("Generating thumbnail...")

    # FFmpeg command to overlay text with the specified font
    ffmpeg_command = (
        f'ffmpeg -y -i "{input_image}" '
        f'-vf "drawtext=text=\'{text}\':'
        f'fontfile=\'{absolute_font_path}\':'
        f'fontcolor=white:fontsize=150:shadowx=10:shadowy=10:shadowcolor=black:x=(w-text_w)/2:y=(h-text_h)/2" '
        f'-frames:v 1 "{output_image}"'
    )
    
    # Run the FFmpeg command
    print("Running FFmpeg command:", ffmpeg_command)
    result = os.system(ffmpeg_command)

    # Check if the thumbnail was generated successfully
    if result == 0:
        print("Thumbnail generated successfully:", output_image)
    else:
        print("Failed to generate thumbnail.")


if __name__ == "__main__":
    # Step 1: Download the image from Google
    search_query = "Rosewood Jeddah hotel booking.com"
    download_image(query=search_query)

    # Step 2: Ensure the input image exists
    input_image = "downloaded_images/000001.jpg"
    if not os.path.exists(input_image):
        print(f"Input image not found at {input_image}")
        exit(1)

    # Step 3: Ensure the font file exists
    font_file = "Nature Beauty Personal Use.ttf"
    if not os.path.exists(font_file):
        print(f"Font file not found at {font_file}")
        exit(1)

    # Step 4: Generate the thumbnail
    generate_thumbnail(input_image=input_image, font_path=font_file)
