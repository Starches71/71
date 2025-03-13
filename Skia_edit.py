import skia
import sys

# Constants
INPUT_IMAGE = "base_image.jpeg"
OUTPUT_IMAGE = "output_with_text.png"
TEXT = "Samsung phones can now flip into two"
FONT_SIZE = 40
FONT_COLOR = skia.ColorWHITE
GRADIENT_COLORS = [skia.ColorWHITE, skia.ColorBLACK]

def apply_gradient_and_text(input_path, output_path):
    # Load image
    surface = skia.Surface.MakeFromImage(skia.Image.open(input_path))
    canvas = surface.getCanvas()

    # Get image dimensions
    width = surface.width()
    height = surface.height()

    # Create gradient paint
    gradient_paint = skia.Paint()
    gradient_paint.setShader(skia.GradientShader.MakeLinear(
        points=[(0, 0), (0, height)],
        colors=GRADIENT_COLORS
    ))
    gradient_paint.setBlendMode(skia.BlendMode.kMultiply)

    # Draw gradient overlay
    canvas.drawRect(skia.Rect.MakeWH(width, height), gradient_paint)

    # Load font
    font = skia.Font(skia.Typeface('Arial', skia.TypefaceStyle.Bold()), FONT_SIZE)
    font.setEdging(skia.Font.Edging.kSubpixelAntiAlias)

    # Measure text width and position
    text_blob = skia.TextBlob.MakeFromString(TEXT, font)
    text_width = font.measureText(TEXT)
    x = (width - text_width) / 2
    y = height - 50  # Position text near the bottom

    # Draw text
    text_paint = skia.Paint(AntiAlias=True, Color=FONT_COLOR)
    canvas.drawTextBlob(text_blob, x, y, text_paint)

    # Save output
    surface.makeImageSnapshot().save(output_path, skia.kPNG)

# Run script
if __name__ == "__main__":
    apply_gradient_and_text(INPUT_IMAGE, OUTPUT_IMAGE)
    print("Image processing complete. Output saved as:", OUTPUT_IMAGE)
