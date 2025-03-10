import cairo
from PIL import Image

# Path to the image in the repo
input_image_path = "images (31).jpeg"
output_image_path = "output_gradient_image.png"

# Open the original image using PIL to get its dimensions
image = Image.open(input_image_path)
width, height = image.size

# Create an image surface from the original image
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
context = cairo.Context(surface)

# Draw the original image onto the Cairo surface
pil_image = image.convert("RGBA")
buffer = pil_image.tobytes("raw", "RGBA", 0, -1)
surface.blit(0, 0, pil_image.width, pil_image.height, cairo.ImageSurface(cairo.FORMAT_ARGB32, pil_image.width, pil_image.height))

# Create a gradient for the bottom part of the image (linear gradient)
gradient = cairo.LinearGradient(0, height - 100, 0, height)  # Gradient starts from 100px above the bottom
gradient.add_color_stop_rgb(0, 0, 0, 1)  # Blue at the bottom
gradient.add_color_stop_rgb(1, 1, 0, 0)  # Red at the very bottom

# Set the gradient as the fill pattern
context.set_source(gradient)

# Paint the gradient at the bottom of the image
context.rectangle(0, height - 100, width, 100)  # Apply gradient to bottom 100px
context.fill()

# Write the modified image to the output path
surface.write_to_png(output_image_path)

print(f"Gradient applied and image saved to {output_image_path}.")
