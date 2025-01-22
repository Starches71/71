
from manim import *

class ThumbnailWithText(Scene):
    def construct(self):
        # Load the image
        image = ImageMobject("downloaded_images/000001.jpg")  # Adjust the image path
        image.scale_to_fit_height(config.frame_height)  # Fit image to frame

        # Add text overlay
        text = Text(
            "Welcome to San Francisco!",
            font="Arial-Bold",
            color=WHITE,
            weight=BOLD
        ).scale(0.5)  # Adjust text size
        text.next_to(image, DOWN, buff=0.5)  # Position text below the image

        # Add the image and text to the scene
        self.add(image, text)

        # Save a static frame (optional)
        self.pause()

# Create a separate function for downloading images
from icrawler.builtin import GoogleImageCrawler

def download_images():
    # Create a GoogleImageCrawler instance
    crawler = GoogleImageCrawler(storage={'root_dir': 'downloaded_images'})
    crawler.crawl(keyword='San Francisco', max_num=10)  # Adjust keyword and max_num as needed

if __name__ == "__main__":
    # Download images
    download_images()

    # Render the thumbnail with Manim
    ThumbnailWithText().render()
