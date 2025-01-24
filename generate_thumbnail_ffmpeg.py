import os
from icrawler.builtin import GoogleImageCrawler

def download_image(query, save_dir="downloaded_images", max_images=1):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    crawler = GoogleImageCrawler(storage={"root_dir": save_dir})
    crawler.crawl(keyword=query, max_num=max_images)
    print(f"Image downloaded as: {save_dir}/000001.jpg")


def generate_thumbnail(input_image="downloaded_images/000001.jpg", 
                       output_image="thumbnail_with_vignette.jpg", 
                       font_path="Nature Beauty Personal Use.ttf"):
    # Check if input image exists
    if not os.path.exists(input_image):
        print(f"Error: Input image '{input_image}' not found.")
        exit(1)
    
    # Check if font file exists
    if not os.path.exists(font_path):
        print(f"Error: Font file '{font_path}' not found.")
        exit(1)

    # Absolute font path
    absolute_font_path = os.path.abspath(font_path)

    # FFmpeg command with vignette effect and formatted text
    ffmpeg_command = (
        f'ffmpeg -y -i "{input_image}" '
        f'-vf "curves=vintage, '
        f'drawtext=text=\'Best Hotels\':'
        f'fontfile=\'{absolute_font_path}\':'
        f'fontcolor=silver:fontsize=350:shadowx=5:shadowy=5:shadowcolor=silver@0.8:'
        f'x=(w-text_w)/2:y=(h-text_h)/3, '
        f'drawtext=text=\'in\':'
        f'fontfile=\'{absolute_font_path}\':'
        f'fontcolor=silver:fontsize=300:shadowx=5:shadowy=5:shadowcolor=silver@0.8:'
        f'x=(w-text_w)/2:y=(h-text_h)/2, '
        f'drawtext=text=\'Jeddah\':'
        f'fontfile=\'{absolute_font_path}\':'
        f'fontcolor=silver:fontsize=300:shadowx=5:shadowy=5:shadowcolor=silver@0.8:'
        f'x=(w-text_w)/2:y=(h+text_h)/2" '
        f'-frames:v 1 "{output_image}"'
    )

    # Debugging: Print and execute FFmpeg command
    print("Running FFmpeg command:", ffmpeg_command)
    result = os.system(ffmpeg_command)

    if result == 0:
        print("Thumbnail generated successfully:", output_image)
    else:
        print("Thumbnail generation failed. Check FFmpeg command or input files.")


if __name__ == "__main__":
    # Step 1: Download the image
    search_query = "Rosewood Jeddah hotel booking.com"
    download_image(query=search_query)

    # Step 2: Verify image and font existence
    input_image = "downloaded_images/000001.jpg"
    font_file = "Nature Beauty Personal Use.ttf"

    if not os.path.exists(input_image):
        print(f"Error: Input image '{input_image}' not found.")
        exit(1)

    if not os.path.exists(font_file):
        print(f"Error: Font file '{font_file}' not found.")
        exit(1)

    # Step 3: Generate the thumbnail
    generate_thumbnail(input_image=input_image, font_path=font_file)
