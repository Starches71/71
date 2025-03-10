
import cv2
import numpy as np

# Load the image
input_image_path = 'images (31).jpeg'
output_image_path = 'output_gradient_image_opencv.png'

# Read the image
image = cv2.imread(input_image_path)

# Get the dimensions of the image
height, width, _ = image.shape

# Create a gradient (linear from blue to red)
gradient = np.zeros((height, width, 3), dtype=np.uint8)

# Define the gradient (simple transition from blue to red at the bottom)
for i in range(height):
    # Calculate the ratio for blending between blue and red
    ratio = i / height
    gradient[i, :, 0] = int(255 * (1 - ratio))  # Blue channel
    gradient[i, :, 2] = int(255 * ratio)        # Red channel

# Apply the gradient to the bottom of the image
gradient_height = 100  # Height of the gradient band
image[height - gradient_height:, :, :] = gradient[height - gradient_height:, :, :]

# Save the output image
cv2.imwrite(output_image_path, image)

print(f"Gradient applied and image saved to {output_image_path}.")
