
import cairo

# Path to the image in the repo
input_image_path = "images (31).jpeg"
output_image_path = "output_gradient_image.png"

# Open the image using Cairo's ImageSurface
image_surface = cairo.ImageSurface.create_from_png(input_image_path)
width = image_surface.get_width()
height = image_surface.get_height()

# Create a context for drawing on the surface
context = cairo.Context(image_surface)

# Draw the original image on the surface
context.set_source_surface(image_surface, 0, 0)
context.paint()

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
image_surface.write_to_png(output_image_path)

print(f"Gradient applied and image saved to {output_image_path}.")
