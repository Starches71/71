
import cv2
import numpy as np

# Load the image
image = cv2.imread("images (31).jpeg")

# Get image dimensions
height, width, _ = image.shape

# Define extra height for text and gradient
extra_height = height // 2  # 50% of original height
new_height = height + extra_height

# Create a new black image (to extend bottom)
extended_image = np.zeros((new_height, width, 3), dtype=np.uint8)
extended_image[:height, :, :] = image  # Place original image on top

# Create gradient effect (fully black at bottom, fading upward)
for i in range(extra_height):
    alpha = 1 - (i / extra_height)  # Alpha decreases as we move up
    extended_image[height + i, :, :] = (np.array([0, 0, 0]) * alpha + 
                                        extended_image[height + i, :, :] * (1 - alpha)).astype(np.uint8)

# Define text parameters
text = "Samsung is the first phone to\nHave built-in 6G in the world"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = min(width / 1000, 1)  # Adjust text size based on width
font_thickness = 2  # Keep text thin for readability
line_spacing = int(50 * font_scale)  # Spacing between lines

# Split text into lines and calculate position
lines = text.split("\n")
total_text_height = len(lines) * line_spacing
text_x = width // 10  # Align text slightly from left
text_y_start = height + (extra_height // 4)  # Start drawing text within gradient

# Put white text over the black gradient (line by line)
for i, line in enumerate(lines):
    text_y = text_y_start + (i * line_spacing)
    cv2.putText(extended_image, line, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

# Save the modified image
cv2.imwrite("output_gradient_image.jpeg", extended_image)

print("Gradient applied and image saved as output_gradient_image.jpeg.")
