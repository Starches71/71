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
def generate_thumbnail(input_image, output_image, text="Best Hotels\n       in\n    Jeddah", font_path="Nature Beauty Personal Use.ttf", color1="#FFD700", color2="#5F9EA0"):
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
        f'fontcolor={color1}:fontsize=150:shadowx=10:shadowy=10:shadowcolor=black:'
        f'x=(w-text_w)/2:y=(h-text_h)/2-100,'
        f'drawtext=text=\'Jeddah\':'
        f'fontfile=\'{font_path}\':'
        f'fontcolor={color2}:fontsize=150:shadowx=10:shadowy=10:shadowcolor=black:'
        f'x=(w-text_w)/2:y=(h-text_h)/2+100,'
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

    # Step 2: Generate thumbnails with different color combinations
    output_image = "thumbnail_with_text_vignette.jpg"
    font_file = "Nature Beauty Personal Use.ttf"  # Font file in the main branch
    
    # Example 1: Using Warm Gold for Best Hotels and Soft Teal for Jeddah (Jeddah brighter)
    generate_thumbnail(input_image, "thumbnail_1.jpg", font_path=font_file, color1="#FFD700", color2="#5F9EA0")
    
    # Example 2: Using Coral for Best Hotels and Aqua for Jeddah (Jeddah brighter)
    generate_thumbnail(input_image, "thumbnail_2.jpg", font_path=font_file, color1="#FF7F50", color2="#00FFFF")
    
    # Example 3: Using Dark Slate Blue for Best Hotels and Light Sky Blue for Jeddah (Jeddah brighter)
    generate_thumbnail(input_image, "thumbnail_3.jpg", font_path=font_file, color1="#483D8B", color2="#87CEFA")
    
    # Example 4: Using Tomato for Best Hotels and Medium Spring Green for Jeddah (Jeddah brighter)
    generate_thumbnail(input_image, "thumbnail_4.jpg", font_path=font_file, color1="#FF6347", color2="#00FA9A")
    
    # Example 5: Using Midnight Blue for Best Hotels and Turquoise for Jeddah (Jeddah brighter)
    generate_thumbnail(input_image, "thumbnail_5.jpg", font_path=font_file, color1="#191970", color2="#40E0D0")
