from PIL import Image, ImageDraw

# Open the image from the repository
im = Image.open('images (31).jpeg')  # Corrected filename

def interpolate(f_co, t_co, interval):
    det_co =[(t - f) / interval for f , t in zip(f_co, t_co)]
    for i in range(interval):
        yield [round(f + det * i) for f, det in zip(f_co, det_co)]

# Create a gradient overlay
gradient = Image.new('RGBA', im.size, color=0)
draw = ImageDraw.Draw(gradient)

# Define start and end colors for the gradient
f_co = (13, 255, 154)  # Starting color (light)
t_co = (4, 128, 30)    # Ending color (dark)

# Apply the gradient to the top 70% of the image
for i, color in enumerate(interpolate(f_co, t_co, im.width * 2)):
    draw.line([(i, 0), (i, int(im.height * 0.7))], tuple(color), width=1)

# Now, apply a black gradient to the bottom 30% of the image
black_start = (0, 0, 0)  # Black color
black_end = (0, 0, 0)    # Black color (no change)

for i, color in enumerate(interpolate(black_start, black_end, im.width * 2)):
    draw.line([(i, int(im.height * 0.7)), (i, im.height)], tuple(color), width=1)

# Composite the gradient over the original image
im_composite = Image.alpha_composite(im.convert('RGBA'), gradient)

# Show the result (for debugging)
im_composite.show()

# Save the final image
im_composite.save('img_result.png')
