import cv2
import numpy as np

# Read the image
image = cv2.imread('images (31).jpeg')

# Get image dimensions
height, width, _ = image.shape

# Define the extra black space to be added (increase for a larger gradient area)
extra_height = height // 3  # Increase image height by 1/3

# Create a black gradient (fading from black to transparent)
gradient = np.zeros((extra_height, width, 3), dtype=np.uint8)
for i in range(extra_height):
    gradient[i, :, :] = (0, 0, 0)  # Fully black

# Stack the gradient below the image
image_with_gradient = np.vstack((image, gradient))

# Define text properties
text = "Samsung S25 becomes first phone to have 6G technology. What an amazing technology!"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1.2
font_thickness = 3
text_color = (255, 255, 255)  # White text
text_position = (50, height + extra_height // 2)  # Position in the gradient

# Add text to the gradient area
cv2.putText(image_with_gradient, text, text_position, font, font_scale, text_color, font_thickness, cv2.LINE_AA)

# Save the final image
cv2.imwrite('output_gradient_image.jpeg', image_with_gradient)

print("Gradient added, text written, and image saved as output_gradient_image.jpeg.")
