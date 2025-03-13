
import skia
import sys
from PIL import Image

# Constants
INPUT_IMAGE = "base_image.jpeg"
OUTPUT_IMAGE = "output_with_text.png"
TEXT = "Samsung phones can now flip into two"
FONT_SIZE = 40
FONT_COLOR = skia.ColorWHITE
GRADIENT_COLORS = [skia.ColorWHITE, skia.ColorBLACK]

def apply_gradient_and_text(input_path, output_path):
    # Load image using PIL to get dimensions
    pil_img = Image.open(input_path)
    width, height = pil_img.size

    # Convert PIL image to Skia image
    skia_image = skia.Image.frombytes(pil_img.tobytes(), width, height, skia.kRGBA_8888_ColorType)

    # Create a new Skia Surface
    surface = skia.Surface.MakeRasterN32Premul(width, height)
    canvas = surface.getCanvas()

    # Draw the original image
    canvas.drawImage(skia_image, 0, 0)

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

    # Save output using PIL (since Skia does not directly save images)
    img_out = Image.frombytes("RGBA", (width, height), surface.makeImageSnapshot().toBytes())
    img_out.save(output_path, "PNG")

# Run script
if __name__ == "__main__":
    apply_gradient_and_text(INPUT_IMAGE, OUTPUT_IMAGE)
    print("Image processing complete. Output saved as:", OUTPUT_IMAGE)
