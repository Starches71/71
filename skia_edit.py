
import skia
import sys
import textwrap

# File paths
INPUT_IMAGE = "base_image.jpeg"
OUTPUT_IMAGE = "output_with_text.png"
TEXT = "Samsung phones can now flip into two"  # Example text
FONT_SIZE = 30  # Adjusted to be smaller
LINE_WIDTH = 25  # Max characters per line

def apply_gradient_and_text(input_path, output_path):
    try:
        # Load the image
        img = skia.Image.open(input_path)

        # Get image dimensions
        width, height = img.width(), img.height()

        # Create a Skia surface matching the image size
        surface = skia.Surface(width, height)
        canvas = surface.getCanvas()

        # Draw the original image onto the canvas
        paint = skia.Paint()
        canvas.drawImage(img, 0, 0)

        # Apply gradient overlay (transparent to black at the bottom)
        gradient_paint = skia.Paint()
        gradient_paint.setShader(
            skia.GradientShader.MakeLinear(
                points=[(0, height * 0.7), (0, height)],  # Apply only to lower 30%
                colors=[skia.ColorBLACK.withAlpha(0), skia.ColorBLACK.withAlpha(180)],
            )
        )
        canvas.drawRect(skia.Rect.MakeWH(width, height), gradient_paint)

        # Prepare text for wrapping
        wrapped_text = textwrap.fill(TEXT, width=LINE_WIDTH)

        # Add text overlay
        font = skia.Font(skia.Typeface('Arial'), FONT_SIZE)
        text_paint = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)

        # Calculate text positioning (centered at the bottom)
        text_x = width * 0.05  # Small left margin
        text_y = height * 0.85  # Adjusted to be above the bottom

        # Draw each line of text
        for line in wrapped_text.split("\n"):
            canvas.drawString(line, text_x, text_y, font, text_paint)
            text_y += FONT_SIZE + 5  # Move down for the next line

        # Save the final image
        image = surface.makeImageSnapshot()
        image.save(output_path, skia.kPNG)

        print("✅ Image processing complete!")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

# Run function
apply_gradient_and_text(INPUT_IMAGE, OUTPUT_IMAGE)
