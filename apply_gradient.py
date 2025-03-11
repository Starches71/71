import cv2
import numpy as np

# Read the image
image = cv2.imread('images (31).jpeg')

# Get image dimensions
height, width, _ = image.shape

# Define extra space for black area + gradient (extra height = 1/3 of image height)
extra_black_height = height // 6  # Pure black part at the bottom
extra_gradient_height = height // 3  # Fading gradient part

# Create a completely black region
black_bar = np.zeros((extra_black_height, width, 3), dtype=np.uint8)

# Create a gradient that starts black and fades upwards
gradient = np.zeros((extra_gradient_height, width, 3), dtype=np.uint8)
for i in range(extra_gradient_height):
    intensity = int(255 * (i / extra_gradient_height))  # Fades from black to transparent
    gradient[i, :, :] = (intensity, intensity, intensity)  # Grayscale fade

# Stack everything: image + gradient + black bar
image_with_gradient = np.vstack((image, gradient, black_bar))

# Define text properties
text = "Samsung S25 becomes first phone to have 6G technology. What an amazing technology!"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_thickness = 2
text_color = (255, 255, 255)  # White text

# Get text size
(text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, font_thickness)

# Center text horizontally
text_x = (width - text_width) // 2  

# Place text inside the black area (ensuring visibility)
text_y = height + extra_gradient_height + extra_black_height // 2 + text_height // 2  

# Draw text
cv2.putText(image_with_gradient, text, (text_x, text_y), font, font_scale, text_color, font_thickness, cv2.LINE_AA)

# Save final image
cv2.imwrite('output_gradient_image.jpeg', image_with_gradient)

print("Final image saved as output_gradient_image.jpeg with proper gradient and text.")
