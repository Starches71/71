
import cv2
import numpy as np

# Load the image
image = cv2.imread("images (31).jpeg")

# Get image dimensions
height, width, _ = image.shape

# Define extra height for text and gradient
extra_height = height // 2  # 50% extra space at the top
new_height = height + extra_height

# Create a new black image (to extend upwards)
extended_image = np.zeros((new_height, width, 3), dtype=np.uint8)
extended_image[extra_height:, :, :] = image  # Place original image on the bottom

# Create a gradient effect (smooth fade from transparent to black upwards)
for i in range(extra_height):
    alpha = (i / extra_height) ** 2  # Strong black at top, fades smoothly
    extended_image[i, :, :] = (np.array([0, 0, 0]) * (1 - alpha) + 
                               extended_image[i, :, :] * alpha).astype(np.uint8)

# Define text parameters
text = "Samsung is the first phone to\nHave built-in 6G in the world"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = min(width / 800, 1.0)  # Slightly larger text, but reasonable size
font_thickness = 2  # Thin text for better readability
line_spacing = int(60 * font_scale)  # Spacing between lines

# Calculate text size and center it
lines = text.split("\n")
text_sizes = [cv2.getTextSize(line, font, font_scale, font_thickness)[0] for line in lines]
max_text_width = max(size[0] for size in text_sizes)
total_text_height = sum(size[1] for size in text_sizes) + (len(lines) - 1) * line_spacing

text_x = (width - max_text_width) // 2  # Center text horizontally
text_y_start = extra_height + (height - total_text_height) // 2  # Center text in gradient area

# Draw text line by line
for i, (line, size) in enumerate(zip(lines, text_sizes)):
    text_y = text_y_start + (i * (size[1] + line_spacing))
    cv2.putText(extended_image, line, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

# Save the modified image
cv2.imwrite("output_gradient_image_upwards_white_text.jpeg", extended_image)

print("Upward gradient applied and image saved as output_gradient_image_upwards_white_text.jpeg.")
