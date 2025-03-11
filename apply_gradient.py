
from PIL import Image, ImageDraw, ImageFont

# Load the image
image = Image.open("images (31).jpeg")

# Get image dimensions
width, height = image.size

# Define extra height for text and gradient
extra_height = height // 2  # 50% extra space at the top
new_height = height + extra_height

# Create a new blank image (to extend upwards)
extended_image = Image.new("RGB", (width, new_height), (0, 0, 0))
extended_image.paste(image, (0, extra_height))  # Place original image at the bottom

# Create a gradient effect (smooth fade from transparent to black upwards)
gradient = Image.new("L", (width, extra_height), color=0)  # Grayscale image for gradient
for i in range(extra_height):
    alpha = (i / extra_height) ** 2  # Strong black at the top, fades smoothly
    gradient.putpixel((0, i), int(255 * alpha))

# Apply gradient to the extended image (fill the top with the gradient)
extended_image.paste(gradient.convert("RGB"), (0, 0))

# Define text parameters
text = "Samsung is the first phone to\nHave built-in 6G in the world"
font = ImageFont.load_default()  # Using default font (no need to specify a TTF file)
font_size = int(min(width / 800, 1.0) * 30)  # Adjust font size based on width
text_color = (255, 255, 255)  # White text color

# Calculate text size and center it
draw = ImageDraw.Draw(extended_image)
lines = text.split("\n")

# Calculate text bounding box for each line
text_widths = [draw.textbbox((0, 0), line, font=font)[2] for line in lines]
max_text_width = max(text_widths)
total_text_height = sum([draw.textbbox((0, 0), line, font=font)[3] for line in lines]) + (len(lines) - 1) * 20

text_x = (width - max_text_width) // 2  # Center text horizontally
text_y_start = extra_height + (height - total_text_height) // 2  # Center text in gradient area

# Draw text line by line
for i, line in enumerate(lines):
    text_y = text_y_start + (i * (draw.textbbox((0, 0), line, font=font)[3] + 20))
    draw.text((text_x, text_y), line, font=font, fill=text_color)

# Save the modified image
extended_image.save("output_gradient_image_upwards_white_text_pillow.jpeg")

print("Upward gradient applied and image saved as output_gradient_image_upwards_white_text_pillow.jpeg.")
