from moviepy.editor import ImageClip, TextClip, CompositeVideoClip
from icrawler.builtin import GoogleImageCrawler

# Step 1: Download Images
def download_images():
    # Create a GoogleImageCrawler instance
    crawler = GoogleImageCrawler(storage={'root_dir': 'downloaded_images'})
    crawler.crawl(keyword='San Francisco', max_num=10)  # Adjust keyword and max_num as needed

# Step 2: Create Thumbnail with Text Overlay
def create_thumbnail(image_path, output_path, text):
    # Load the image
    image = ImageClip(image_path)

    # Create the text overlay
    text_overlay = TextClip(text, fontsize=70, color='white', font='Arial-Bold') \
        .set_position(('center', 'bottom')) \
        .set_duration(10)  # Set duration (not critical for static image)

    # Combine the image and text overlay
    final_thumbnail = CompositeVideoClip([image, text_overlay])

    # Save the final thumbnail as an image
    final_thumbnail.save_frame(output_path)
    print(f"Thumbnail saved to: {output_path}")

if __name__ == "__main__":
    # Download images
    download_images()

    # Path to the first downloaded image
    input_image = "downloaded_images/000001.jpg"  # Adjust based on your folder's structure
    output_thumbnail = "thumbnail_with_text.jpg"

    # Generate a thumbnail with text overlay
    create_thumbnail(input_image, output_thumbnail, "Welcome to San Francisco!")
