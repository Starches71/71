
from PIL import Image, ImageDraw

# Open the input image
im = Image.open('31.jpeg')

# Function to interpolate between two colors
def interpolate(f_co, t_co, interval):
    det_co =[(t - f) / interval for f , t in zip(f_co, t_co)]
    for i in range(interval):
        yield [round(f + det * i) for f, det in zip(f_co, det_co)]

# Create a new image with the same size as the original image for the gradient
gradient = Image.new('RGBA', im.size, color=0)
draw = ImageDraw.Draw(gradient)

# Define the gradient color (black for the bottom 30% of the image)
f_co = (0, 0, 0, 0)  # Transparent (start of the gradient)
t_co = (0, 0, 0, 255)  # Black (end of the gradient)
for i, color in enumerate(interpolate(f_co, t_co, int(im.width))):
    draw.line([(i, im.height * 0.7), (i, im.height)], tuple(color), width=1)

# Composite the gradient onto the original image
im_composite = Image.alpha_composite(im.convert('RGBA'), gradient)

# Save the result
im_composite.show()
im_composite.save('img_result.png')
