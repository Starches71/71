
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip

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
    input_image = "downloaded_images/000001.jpg"  # Adjust to your image path
    output_image = "output/thumbnail_with_text.png"
    generate_thumbnail(input_image, output_image)
