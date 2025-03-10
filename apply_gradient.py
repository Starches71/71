
import cv2
import numpy as np

# Read the image
image = cv2.imread('images (31).jpeg')

# Get image dimensions
height, width, _ = image.shape

# Define extra space for the gradient (1/3 of image height)
extra_height = height // 3  

# Create a black gradient (darkest at bottom, fading upward)
gradient = np.zeros((extra_height, width, 3), dtype=np.uint8)
for i in range(extra_height):
    intensity = int(255 * (i / extra_height))  # Gradually fade from black to transparent
    gradient[i, :, :] = (intensity, intensity, intensity)  # Grayscale fading

# Stack gradient below the image
image_with_gradient = np.vstack((image, gradient))

# Define text properties
text = "Samsung S25 becomes first phone to have 6G technology. What an amazing technology!"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_thickness = 2
text_color = (255, 255, 255)  # White text

# Get text size to center it
(text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, font_thickness)
text_x = (width - text_width) // 2  # Center horizontally
text_y = height + extra_height // 2 + text_height // 2  # Place in the middle of gradient

# Draw text on gradient
cv2.putText(image_with_gradient, text, (text_x, text_y), font, font_scale, text_color, font_thickness, cv2.LINE_AA)

# Save the final image
cv2.imwrite('output_gradient_image.jpeg', image_with_gradient)

print("Gradient added, text written, and image saved as output_gradient_image.jpeg.")
