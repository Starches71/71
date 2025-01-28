
import os                               import subprocess

# Directories
best_clip2 = "best_clip2"
best = "best"                           output_dir = "best_clip3"               htl11_script = "htl11.py"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to find the first .txt file in the `best` directory
def find_text_file(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            return os.path.join(directory, filename)
    return None

# Function to add text overlays with typing effect and shadow background
def add_text_overlay(input_file, text1, text2, duration, output_file):
    # Define reveal speed (0.5 seconds for each text)
    reveal_speed = 0.5

    # Overlay for the first text (hotel name with typing effect)
    first_text_duration = reveal_speed
    first_text_static_duration = duration / 2 - reveal_speed
    first_half_overlay = (
        f"drawtext=text='{text1}':fontfile=/storage/emulated/0/Download/FontsFree-Net-Proxima-Nova-Bold-It.otf.ttf:"
        f"fontsize=30:fontcolor=white:shadowcolor=black:shadowx=3:shadowy=3:"
        f"x='if(lt(t,{first_text_duration}),-tw+(t*tw/{first_text_duration}),10)':"
        f"y=H-50:enable='lt(t,{duration / 2})'"
    )

    # Overlay for the second text (link with typing effect)
    second_text_start = duration / 2
    second_text_duration = second_text_start + reveal_speed
    second_text_static_duration = duration - second_text_start - reveal_speed
    second_half_overlay = (
        f"drawtext=text='{text2}':fontfile=/storage/emulated/0/Download/FontsFree-Net-Proxima-Nova-Bold-It.otf.ttf:"
        f"fontsize=30:fontcolor=white:shadowcolor=black:shadowx=3:shadowy=3:"
        f"x='if(lt(t,{second_text_duration}),-tw+((t-{second_text_start})*tw/{reveal_speed}),10)':"
        f"y=H-50:enable='gte(t,{second_text_start})'"
    )

    # Combine both overlays
    overlay_text = f"{first_half_overlay},{second_half_overlay}"

    # FFmpeg command
    command = [
        "ffmpeg", "-i", input_file, "-vf", overlay_text,
        "-c:v", "libx264", "-crf", "23", "-preset", "fast", "-y", output_file
    ]
    print(f"Overlays added to: {output_file}")

# Main function to process all videos
def main():
    # Find the text file
    text_file = find_text_file(best)
    if not text_file:
        print("No .txt file found in the best directory.")
        return

    with open(text_file, 'r') as file:
        hotel_names = file.read().splitlines()

    video_files = sorted(os.listdir(best_clip2))
    if len(hotel_names) != len(video_files):
        print("Number of hotel names does not match the number of videos in best_clip2.")
        return

    for idx, video in enumerate(video_files):
        video_path = os.path.join(best_clip2, video)
        hotel_name = hotel_names[idx]
        output_path = os.path.join(output_dir, video)

        # Extract video duration
        ffprobe_cmd = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", video_path
        ]
        duration = float(subprocess.check_output(ffprobe_cmd).strip())

        # Overlay texts
        link_text = "Link of the hotel in description ↓"
        add_text_overlay(video_path, hotel_name, link_text, duration, output_path)

    # Activate `htl11.py` after applying text overlays
    try:
        print(f"Successfully activated {htl11_script}.")
    except subprocess.CalledProcessError as e:
        print(f"Error running {htl11_script}: {e}")

if __name__ == "__main__":
    main()
