
import os
from icrawler.builtin import GoogleImageCrawler

# Step 1: Download the image
def download_image(search_term, output_dir="downloaded_images"):
    os.makedirs(output_dir, exist_ok=True)
    crawler = GoogleImageCrawler(storage={"root_dir": output_dir})
    crawler.crawl(keyword=search_term, max_num=1)
    print("Image downloaded as:", os.path.join(output_dir, "000001.jpg"))
    return os.path.join(output_dir, "000001.jpg")

# Step 2: Generate a thumbnail using FFmpeg with silver text and shadow
def generate_thumbnail(input_image, output_image, text="Welcome to San Francisco!", font_path="rock_stencil.ttf"):
    ffmpeg_command = (
        f'ffmpeg -y -i "{input_image}" '
        f'-vf "drawtext=text=\'{text}\':'
        f'fontfile=\'{font_path}\':'
        f'fontcolor=silver:fontsize=48:shadowx=3:shadowy=3:shadowcolor=black:x=(w-text_w)/2:y=(h-text_h)-50" '
        f'"{output_image}"'
    )
    print("Running FFmpeg command:", ffmpeg_command)
    result = os.system(ffmpeg_command)
    if result == 0:
        print("Thumbnail generated successfully:", output_image)
    else:
        print("Failed to generate thumbnail.")

if __name__ == "__main__":
    # Step 1: Download an image
    search_query = "San Francisco cityscape"
    input_image = download_image(search_query)

    # Step 2: Generate thumbnail with overlay text, silver font, and shadow
    output_image = "thumbnail_with_text.jpg"
    font_file = "rock_stencil.ttf"  # Path to the downloaded font
    generate_thumbnail(input_image, output_image, font_path=font_file)
