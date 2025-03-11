import cv2
import numpy as np

# Load the image
image = cv2.imread("images (31).jpeg")

# Get image dimensions
height, width, _ = image.shape

# Define extra height for text and gradient
extra_height = height // 3  # 33% of the original height
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
text = "Samsung S25 becomes first phone with 6G technology!"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = min(width / 800, 1)  # Adjust text size based on width
font_thickness = 2
text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]

# Calculate text position (centered horizontally, inside the black area)
text_x = (width - text_size[0]) // 2
text_y = height + extra_height // 2 + text_size[1] // 2

# Put white text over the black gradient
cv2.putText(extended_image, text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

# Save the modified image
cv2.imwrite("output_gradient_image.jpeg", extended_image)

print("Gradient applied and image saved as output_gradient_image.jpeg.")
