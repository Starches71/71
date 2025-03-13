import skia
import sys

# Input and output file names
INPUT_IMAGE = "base_image.jpeg"
OUTPUT_IMAGE = "output_with_text.png"

def apply_gradient_and_text(input_path, output_path):
    # Load image using Skia
    try:
        image = skia.Image.MakeFromEncoded(skia.Data.MakeFromFileName(input_path))
        if not image:
            raise ValueError("Failed to load image with Skia.")

        width, height = image.width(), image.height()
        print(f"Loaded image with Skia: {width}x{height}")

        # Create surface with the same dimensions
        surface = skia.Surface(width, height)
        canvas = surface.getCanvas()

        # Draw the original image
        paint = skia.Paint()
        canvas.drawImage(image, 0, 0, paint)

        # Create a gradient overlay
        gradient_paint = skia.Paint()
        gradient_shader = skia.GradientShader.MakeLinear(
            points=[(0, 0), (0, height)],
            colors=[skia.ColorWHITE, skia.ColorBLACK],
            mode=skia.TileMode.CLAMP,
        )
        gradient_paint.setShader(gradient_shader)
        canvas.drawPaint(gradient_paint)

        # Draw text on the image
        font = skia.Font(skia.Typeface('Arial'), 30)
        text_paint = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        text = "Samsung phones can now flip into two"
        text_blob = skia.TextBlob.MakeFromString(text, font)
        text_x = (width - font.measureText(text)) / 2
        text_y = height - 40
        canvas.drawTextBlob(text_blob, text_x, text_y, text_paint)

        # Save output
        image_snapshot = surface.makeImageSnapshot()
        image_data = image_snapshot.encodeToData()
        if image_data:
            with open(output_path, "wb") as f:
                f.write(image_data.bytes())
        print(f"Saved output image: {output_path}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

# Run function
apply_gradient_and_text(INPUT_IMAGE, OUTPUT_IMAGE)
