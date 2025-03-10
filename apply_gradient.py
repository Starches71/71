
import cv2
import numpy as np

# Read the image from the repository folder (it will be fetched by GitHub Actions)
image = cv2.imread('images (31).jpeg')

# Get image dimensions
height, width, _ = image.shape

# Create a gradient (you can change the colors or type of gradient)
gradient = np.zeros((height//4, width, 3), dtype=np.uint8)
for i in range(height//4):
    gradient[i, :, :] = (0, 0, int(255 * (i / (height//4))))  # gradient effect from black to blue

# Combine the gradient with the original image
image_with_gradient = np.vstack((image, gradient))  # Stack the gradient at the bottom

# Save the modified image
cv2.imwrite('output_gradient_image.jpeg', image_with_gradient)

print("Gradient applied and image saved as output_gradient_image.jpeg.")
