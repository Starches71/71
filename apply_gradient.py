
from PIL import Image, ImageDraw

def apply_gradient_effect(image_path, output_path):
    # Open the image
    image = Image.open(image_path)
    width, height = image.size
    draw = ImageDraw.Draw(image)

    # Gradient parameters
    gradient_height = 100  # Height of the gradient box at the bottom
    for y in range(height - gradient_height, height):
        r = int((y / height) * 255)  # Gradually change the red intensity
        b = 255 - r  # Gradually change the blue intensity
        draw.line((0, y, width, y), fill=(r, 0, b))

    # Save the modified image
    image.save(output_path)

if __name__ == "__main__":
    input_image = 'images(31).jpeg'
    output_image = 'output_gradient_image.jpeg'
    apply_gradient_effect(input_image, output_image)
