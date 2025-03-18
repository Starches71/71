
import os
import subprocess

# Directories
input_dir = "best_io2"
output_dir = "best_io3"
text_overlay = "Link of all hotels found in description below"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)
print(f"Output directory '{output_dir}' is ready.")

def add_text_overlay(input_file, output_file, text):
    """Adds a text overlay with black outline around the white text to the input video and saves it to the output file."""
    print(f"Adding text overlay to: {input_file}")
    
    # Text overlay filter with black outline around the white text
    overlay_filter = (
        f"drawtext=text='{text}':fontfile=/storage/emulated/0/Download/FontsFree-Net-Proxima-Nova-Bold-It.otf.ttf:"
        f"fontsize=90:fontcolor=white:borderw=3:bordercolor=black:x=(w-text_w)/2:y=h-th-30"
    )

    command = [
        "ffmpeg", "-i", input_file, "-vf", overlay_filter,
        "-c:v", "libx264", "-crf", "23", "-preset", "fast", "-y", output_file
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Overlay added to: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error adding overlay to {input_file}: {e}")

def main():
    # List all video files in the input directory
    print(f"Scanning input directory: {input_dir}")
    video_files = [f for f in os.listdir(input_dir) if f.endswith(".mp4")]

    if not video_files:
        print("No video files found in the input directory.")
        return

    for video in video_files:
        input_path = os.path.join(input_dir, video)
        output_path = os.path.join(output_dir, video)

        # Add text overlay to the video
        add_text_overlay(input_path, output_path, text_overlay)

if __name__ == "__main__":
    main()
