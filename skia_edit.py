
import skia
import sys

# File paths
INPUT_IMAGE = "base_image.jpeg"
OUTPUT_IMAGE = "output_with_text.png"
TEXT = "Samsung phones can now flip into two"
FONT_SIZE = 40  # Adjust based on your needs

def apply_gradient_and_text(input_path, output_path):
    try:
        # Load image
        img = skia.Image.open(input_path)

        # Get image dimensions
        width, height = img.width(), img.height()

        # Create a Skia surface
        surface = skia.Surface(width, height)
        canvas = surface.getCanvas()

        # Draw original image
        paint = skia.Paint()
        canvas.drawImage(img, 0, 0)

        # Apply gradient overlay
        gradient_paint = skia.Paint()
        gradient_paint.setShader(
            skia.GradientShader.MakeLinear(
                points=[(0, 0), (0, height)],
                colors=[skia.ColorWHITE, skia.ColorBLACK],
            )
        )
        canvas.drawRect(skia.Rect.MakeWH(width, height), gradient_paint)

        # Add text overlay
        font = skia.Font(skia.Typeface('Arial'), FONT_SIZE)
        text_paint = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        text_width = font.measureText(TEXT)
        text_x = (width - text_width) / 2
        text_y = height - 50  # Adjust positioning
        canvas.drawString(TEXT, text_x, text_y, font, text_paint)

        # Save final image
        image = surface.makeImageSnapshot()
        image.save(output_path, skia.kPNG)

        print("✅ Image processing complete!")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

# Run function
apply_gradient_and_text(INPUT_IMAGE, OUTPUT_IMAGE)
