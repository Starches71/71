
from remotion import Image, Text, Composition

# Load the image
image = Image("downloaded_images/000001.jpg")  # Adjust the image path
image = image.resize(height=720)  # Resize to fit the height of 720p

# Create a text overlay
text = Text("Welcome to San Francisco!", font_size=50, color="white", font="Arial-Bold")
text = text.align("center").set_position((0, -250))  # Position text below the image

# Create a composition (this is like a canvas for the image and text)
composition = Composition([image, text])

# Export the result as an image (not a video)
composition.export("output/thumbnail_with_text.png")
