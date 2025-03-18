import skia

def apply_gradient_and_text(input_path, output_path):
    # Load the image from the file
    image = skia.Image.open(input_path)
    if image is None:
        raise ValueError("Failed to load image.")

    # Create a surface to draw on
    surface = skia.Surface(image.width(), image.height())
    canvas = surface.getCanvas()

    # Apply a linear gradient
    paint = skia.Paint()
    paint.setShader(skia.Shader.MakeLinearGradient(
        (0, 0), (image.width(), image.height()),
        [skia.Color(255, 255, 255), skia.Color(0, 0, 0)],
        [0, 1],
        skia.TileMode.kClamp_TileMode
    ))
    canvas.drawPaint(paint)

    # Draw the original image onto the canvas
    canvas.drawImage(image, 0, 0)

    # Set up the paint for text
    text_paint = skia.Paint()
    text_paint.setAntiAlias(True)
    text_paint.setColor(skia.Color(255, 255, 255))
    text_paint.setTextSize(12)  # Adjusted font size
    text_paint.setTextAlign(skia.Paint.kCenter_Align)

    # Define the text to overlay
    text = "Samsung phones can now flip into two"

    # Create a font object
    font = skia.Font(skia.Typeface(''), 12)  # Adjusted font size

    # Calculate text bounds
    bounds = skia.Rect()
    font.measureText(text, len(text), skia.TextEncoding.kUTF8, bounds)
    x = (image.width() - bounds.width()) / 2
    y = image.height() - bounds.height() - 10

    # Draw the text onto the canvas
    canvas.drawString(text, x, y, font, text_paint)

    # Save the modified image
    surface.makeImageSnapshot().encodeToData().save(output_path)

if __name__ == '__main__':
    input_image_path = 'images/images (31).jpeg'
    output_image_path = 'output_image.jpeg'
    apply_gradient_and_text(input_image_path, output_image_path)
    print(f"Image saved to {output_image_path}")
