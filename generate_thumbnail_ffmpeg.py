
from icrawler.builtin import GoogleImageCrawler
import os
import subprocess

def download_image(search_query, output_dir):
    """Download the first image from Google Images based on the search query."""
    crawler = GoogleImageCrawler(storage={"root_dir": output_dir})
    crawler.crawl(keyword=search_query, max_num=1)
    image_files = os.listdir(output_dir)
    if image_files:
        print(f"Image downloaded as: {output_dir}/{image_files[0]}")
        return os.path.join(output_dir, image_files[0])
    else:
        print("No image downloaded.")
        return None

def generate_thumbnail(input_image, output_image, hotel_name, location):
    """Generate a thumbnail using FFmpeg."""
    ffmpeg_command = [
        "ffmpeg",
        "-y",
        "-i", input_image,
        "-vf",
        f"""
        format=yuv420p,
        drawbox=x=(w-text_w)/2-20:y=(h-text_h)/2-120:w=text_w+40:h=text_h+40:color=black@0.8:t=fill,
        drawtext=text='{hotel_name}':fontfile='Nature Beauty Personal Use.ttf':fontcolor=white:fontsize=150:shadowx=2:shadowy=2:x=(w-text_w)/2:y=(h-text_h)/2-100,
        drawbox=x=(w-text_w)/2-20:y=(h-text_h)/2+80:w=text_w+40:h=text_h+40:color=black@0.8:t=fill,
        drawtext=text='{location}':fontfile='Nature Beauty Personal Use.ttf':fontcolor=white:fontsize=150:shadowx=2:shadowy=2:x=(w-text_w)/2:y=(h-text_h)/2+100
        """,
        output_image,
    ]

    try:
        subprocess.run(ffmpeg_command, check=True, shell=False)
        print(f"Thumbnail generated successfully: {output_image}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to generate thumbnail. Error: {e}")

if __name__ == "__main__":
    search_query = "Rosewood Jeddah hotel booking.com"
    output_dir = "downloaded_images"
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Download image
    input_image = download_image(search_query, output_dir)

    # Step 2: Generate thumbnail if an image was downloaded
    if input_image:
        output_image = "thumbnail_with_lines.jpg"
        hotel_name = "Best Hotels"
        location = "Jeddah"
        generate_thumbnail(input_image, output_image, hotel_name, location)
