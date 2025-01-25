
import os
from icrawler.builtin import GoogleImageCrawler

# Step 1: Download the image
def download_image(search_term, output_dir="downloaded_images"):
    os.makedirs(output_dir, exist_ok=True)
    crawler = GoogleImageCrawler(storage={"root_dir": output_dir})
    crawler.crawl(keyword=search_term, max_num=1)
    print("Image downloaded as:", os.path.join(output_dir, "000001.jpg"))
    return os.path.join(output_dir, "000001.jpg")

# Step 2: Generate a thumbnail using FFmpeg with lowercase text
def generate_thumbnail(input_image, output_image, text="best hotels\n       in\n     jeddah", font_path="Nature Beauty Personal Use.ttf"):
    # Apply darkening and text overlay
    ffmpeg_command = (
        f'ffmpeg -y -i "{input_image}" '
        f'-vf "format=yuv420p,'
        f'colorchannelmixer=.8:.0:.0:.0:.0:.8:.0:.0:.0:.0:.8:.0,'
        f'drawtext=text=\'{text}\':'
        f'fontfile=\'{font_path}\':'
        f'fontcolor=#C0C0C0:fontsize=96:shadowx=10:shadowy=10:shadowcolor=black:x=(w-text_w)/2:y=(h-text_h)/2,'
        f'lenscorrection=k1=-0.5:k2=0.3" '
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
    search_query = "Rosewood Jeddah hotel booking.com"
    input_image = download_image(search_query)

    # Step 2: Generate thumbnail with lowercase text, darkening, and vignette effect
    output_image = "thumbnail_with_text_vignette.jpg"
    font_file = "Nature Beauty Personal Use.ttf"  # Font file in the main branch
    generate_thumbnail(input_image, output_image, font_path=font_file)
