
import os
import subprocess                       
# Directories                           input_dir = "best_io2"
output_dir = "best_io3"
text_overlay = "Link of all hotels found in description below"
script_to_activate = "htl12.py"
                                        # Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)  
def add_text_overlay(input_file, output_file, text):
    # Sliding text overlay filter with increased font size and shadow adjustments
    overlay_filter = (
        f"drawtext=text='{text}':fontfile=/storage/emulated/0/Download/FontsFree-Net-Proxima-Nova-Bold-It.otf.ttf:"
        f"fontsize=90:fontcolor=#C0C0C0:box=1:boxcolor=black@0.8:boxborderw=5:x=(w-text_w)/2:y=h-th-30:"
        f"shadowcolor=black:shadowx=3:shadowy=3:enable='gte(t,0)'"
    )

    command = [
        "ffmpeg", "-i", input_file, "-vf", overlay_filter,
        "-c:v", "libx264", "-crf", "23", "-preset", "fast", "-y", output_file
    ]
    print(f"Overlay added to: {output_file}")

def main():
    # List all video files in input directory
    video_files = [f for f in os.listdir(input_dir) if f.endswith(".mp4")]

    if not video_files:
        print("No video files found in the input directory.")
        return

    for video in video_files:
        input_path = os.path.join(input_dir, video)
        output_path = os.path.join(output_dir, video)

        # Add text overlay to video
        add_text_overlay(input_path, output_path, text_overlay)

    # Activate htl12.py
    try:
        print(f"Successfully activated {script_to_activate}.")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_to_activate}: {e}")

if __name__ == "__main__":
    main()
