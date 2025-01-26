
import os
from icrawler.builtin import GoogleImageCrawler

# Step 1: Download the image
def download_image(search_term, output_dir="downloaded_images"):
    os.makedirs(output_dir, exist_ok=True)
    crawler = GoogleImageCrawler(storage={"root_dir": output_dir})
    crawler.crawl(keyword=search_term, max_num=1)
    print("Image downloaded as:", os.path.join(output_dir, "000001.jpg"))
    return os.path.join(output_dir, "000001.jpg")

# Step 2: Generate a thumbnail using FFmpeg with vignette and formatted text (brighter text and adjusted size)
def generate_thumbnail(input_image, output_image, text="Best Hotels\n       Jeddah", font_path="Nature Beauty Personal Use.ttf"):
    # Check if the font exists
    if not os.path.exists(font_path):
        print("Font file not found! Please provide a valid path to the font.")
        return

    # FFmpeg command to apply text, shadow, vignette, and darken edges
    ffmpeg_command = (
        f'ffmpeg -y -i "{input_image}" '
        f'-vf "format=yuv420p,'
        f'curves=preset=lighter,'  # Apply curve to lighten the overall image
        f'drawtext=text=\'Best Hotels\':'
        f'fontfile=\'{font_path}\':'
        f'fontcolor=#FFD800:fontsize=150:shadowx=10:shadowy=10:shadowcolor=black:'  # School bus yellow (#FFD800), larger font size
        f'x=(w-text_w)/2:y=(h-text_h)/2-100,'
        f'drawtext=text=\'Jeddah\':'
        f'fontfile=\'{font_path}\':'
        f'fontcolor=#FFD800:fontsize=150:shadowx=10:shadowy=10:shadowcolor=black:'  # Same text styling for Jeddah
        f'x=(w-text_w)/2:y=(h-text_h)/2+100,'  # Adjust y-position to align Jeddah below Best Hotels
        f'vignette=PI/4:enable=\'between(t,0,5)\'" '  # Vignette filter applied at the edges
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

    # Step 2: Generate thumbnail with "Best Hotels" and "Jeddah" in school bus yellow and black shadow with vignette effect
    output_image = "thumbnail_with_text_vignette.jpg"
    font_file = "Nature Beauty Personal Use.ttf"  # Font file in the main branch
    generate_thumbnail(input_image, output_image, font_path=font_file)
