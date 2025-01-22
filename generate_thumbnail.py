
from icrawler.builtin import GoogleImageCrawler
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip
import os

def download_image_with_icrawler(keyword, save_dir, image_name):
    os.makedirs(save_dir, exist_ok=True)
    crawler = GoogleImageCrawler(storage={'root_dir': save_dir})
    crawler.crawl(keyword=keyword, max_num=1)  # Download only one image
    # Rename the first downloaded image to match the desired name
    for file in os.listdir(save_dir):
        if file.endswith(('.jpg', '.png', '.jpeg')):
            os.rename(os.path.join(save_dir, file), os.path.join(save_dir, image_name))
            print(f"Image downloaded as: {os.path.join(save_dir, image_name)}")
            break

def generate_thumbnail(image_path, output_path):
    # Load the image
    image_clip = ImageClip(image_path).resize((1280, 720))
    
    # Create the text overlay
    text = "Welcome to San Francisco!"
    text_clip = TextClip(
        text,
        fontsize=50,
        color='white',
        font='Arial-Bold',
        bg_color=None,
        size=None,
    ).set_position(("center", "bottom")).margin(bottom=100).set_duration(1)
    
    # Composite image and text
    thumbnail = CompositeVideoClip([image_clip, text_clip]).set_duration(1)
    
    # Save the result as an image
    thumbnail.save_frame(output_path, t=0)
    print(f"Thumbnail generated and saved to: {output_path}")

if __name__ == "__main__":
    keyword = "San Francisco cityscape"  # Replace with your search keyword
    save_dir = "downloaded_images"
    image_name = "000001.jpg"
    input_image = os.path.join(save_dir, image_name)
    output_image = "output/thumbnail_with_text.png"
    
    # Download the image using icrawler
    download_image_with_icrawler(keyword, save_dir, image_name)
    
    # Generate the thumbnail
    generate_thumbnail(input_image, output_image)
