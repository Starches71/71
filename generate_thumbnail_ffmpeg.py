import os
import subprocess

# Define paths
input_image_dir = "downloaded_images"
output_image = "thumbnail_with_vignette.jpg"
text = "Explore the Best Hotels in Jamaica!"  # Customize your text
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Update this to the path of your font

# Ensure the input directory exists
if not os.path.exists(input_image_dir):
    print(f"Directory '{input_image_dir}' does not exist.")
    exit(1)

# Find the first image in the directory
input_images = [f for f in os.listdir(input_image_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
if not input_images:
    print("No images found in 'downloaded_images' directory.")
    exit(1)

input_image = os.path.join(input_image_dir, input_images[0])

# Check if FFmpeg is installed
try:
    subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
except FileNotFoundError:
    print("FFmpeg is not installed or not found in PATH.")
    exit(1)

# Apply vignette effect and add text overlay
ffmpeg_command = [
    "ffmpeg", "-y", "-i", input_image, "-vf",
    f"vignette,drawtext=fontfile={font_path}:text='{text}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/1.2",
    output_image
]

try:
    subprocess.run(ffmpeg_command, check=True)
    print(f"Thumbnail with vignette effect and text created: {output_image}")
except subprocess.CalledProcessError as e:
    print(f"Error generating thumbnail: {e}")
    exit(1)
