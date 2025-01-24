import os
import logging
from icrawler.builtin import GoogleImageCrawler
import subprocess

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create directories for downloaded images
os.makedirs("downloaded_images", exist_ok=True)

# Image search and download
search_term = "Rosewood Jeddah hotel booking.com"
google_crawler = GoogleImageCrawler(storage={"root_dir": "downloaded_images"})
google_crawler.crawl(keyword=search_term, max_num=1)

# Check if any image was downloaded
image_path = os.path.join("downloaded_images", "000001.jpg")
if not os.path.isfile(image_path):
    logging.error("Image download failed!")
    exit(1)

# Define output file path
output_path = "thumbnail_with_vignette.jpg"

# FFmpeg command to add vignette and styled text
ffmpeg_command = [
    "ffmpeg", "-y",
    "-i", image_path,
    "-vf",
    (
        "curves=vintage, "
        "drawtext=text='Best Hotels':fontfile='Nature Beauty Personal Use.ttf':"
        "fontcolor=silver:fontsize=350:shadowx=5:shadowy=5:shadowcolor=silver@0.8:"
        "x=(w-text_w)/2:y=(h-text_h)/3, "
        "drawtext=text='in':fontfile='Nature Beauty Personal Use.ttf':"
        "fontcolor=silver:fontsize=300:shadowx=5:shadowy=5:shadowcolor=silver@0.8:"
        "x=(w-text_w)/2:y=(h-text_h)/2, "
        "drawtext=text='Jeddah':fontfile='Nature Beauty Personal Use.ttf':"
        "fontcolor=silver:fontsize=300:shadowx=5:shadowy=5:shadowcolor=silver@0.8:"
        "x=(w-text_w)/2:y=(h+text_h)/2"
    ),
    "-frames:v", "1", output_path
]

# Run FFmpeg command
try:
    subprocess.run(ffmpeg_command, check=True)
    logging.info(f"Thumbnail generated successfully: {output_path}")
except subprocess.CalledProcessError as e:
    logging.error(f"FFmpeg command failed: {e}")
    exit(1)
