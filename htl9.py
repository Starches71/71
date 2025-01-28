
import os
import subprocess

# Configuration for consistent video properties
TARGET_WIDTH = 640
TARGET_HEIGHT = 360
FRAME_RATE = 30
SAR = "1:1"

# Function to check if a file is valid for processing
def check_and_add_file(file_path, valid_videos):
    """
    Validates if the given file is a valid video:
    - File exists
    - File size > 0
    - File name does not contain 'silenced_'
    - File contains a valid video stream
    """
    if os.path.isfile(file_path) and os.path.getsize(file_path) > 0 and "silenced_" not in file_path:
        # Check if the file contains a video stream using FFmpeg
            ['ffmpeg', '-i', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if b"Video:" in result.stderr:
            valid_videos.append(file_path)
        else:
            print(f"Skipping file without video stream: {file_path}")
    else:
        print(f"Skipping invalid or empty file: {file_path}")

# Function to scale videos to the same resolution, SAR, and frame rate
def scale_video(input_file, output_file):
    """
    Scales the input video to the target resolution, SAR, and frame rate.
    """
    command = [
        "ffmpeg", "-i", input_file,
        "-vf", f"scale={TARGET_WIDTH}:{TARGET_HEIGHT},setsar={SAR},fps={FRAME_RATE}",
        "-c:v", "libx264", "-crf", "23", "-preset", "fast", "-y",  # Re-encode video
        output_file
    ]
    print(f"Scaled video saved to: {output_file}")

# Function to concatenate videos with re-encoding
def concatenate_videos_reencode(input_videos, output_file):
    """
    Concatenates a list of input videos into a single output file using FFmpeg.
    Re-encoding is applied to avoid duration mismatches.
    """
    filter_complex = "".join(f"[{i}:v:0]" for i in range(len(input_videos)))
    filter_complex += f"concat=n={len(input_videos)}:v=1:a=0[outv]"

    command = ["ffmpeg", "-y"]  # Overwrite output file if it exists
    for video in input_videos:
        command.extend(["-i", video])
    command.extend(["-filter_complex", filter_complex, "-map", "[outv]", output_file])

    print(f"Concatenated videos saved to: {output_file}")

# Function to activate another script, `htl10.py`
def activate_htl10():
    """
    Activates the script `htl10.py` after processing all groups.
    """
    try:
        print("Activating htl10.py...")
        print("htl10.py activated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error activating htl10.py: {e}")

# Ensure the output directory exists
os.makedirs('best_join', exist_ok=True)
os.makedirs('scaled_videos', exist_ok=True)

# Function to process each group of videos
def process_group(group_number):
    """
    Processes a specific group of videos by:
    - Validating video files
    - Scaling videos to consistent properties
    - Concatenating valid videos
    - Writing the output to the 'best_join' directory
    """
    group_file = f'group{group_number}.txt'
    scaled_videos = []

    # Define input files for the current group
    input_videos = [
        f"best_vid_clean/{group_number}A.a.mp4", f"best_vid_clean/{group_number}B.a.mp4", f"best_vid_clean/{group_number}C.a.mp4",
        f"best_vid_clean/{group_number}A.b.mp4", f"best_vid_clean/{group_number}B.b.mp4", f"best_vid_clean/{group_number}C.b.mp4",
        f"best_vid_clean/{group_number}A.c.mp4", f"best_vid_clean/{group_number}B.c.mp4", f"best_vid_clean/{group_number}C.c.mp4",
        f"best_vid_clean/{group_number}A.d.mp4", f"best_vid_clean/{group_number}B.d.mp4", f"best_vid_clean/{group_number}C.d.mp4",
        f"best_vid_clean/{group_number}A.e.mp4", f"best_vid_clean/{group_number}B.e.mp4", f"best_vid_clean/{group_number}C.e.mp4"
    ]

    # Validate input videos
    valid_videos = []
    for file in input_videos:
        check_and_add_file(file, valid_videos)

    # Scale videos and prepare for concatenation
    for video in valid_videos:
        scaled_video = f"scaled_videos/scaled_{os.path.basename(video)}"
        scale_video(video, scaled_video)
        scaled_videos.append(scaled_video)

    # Concatenate videos if valid files exist
    if scaled_videos:
        output_file = f'best_join/{group_number}.mp4'
        concatenate_videos_reencode(scaled_videos, output_file)
    else:
        print(f"No valid videos found for group {group_number}")

# Process all groups from 1 to 7
for group_number in range(1, 8):
    process_group(group_number)

# After processing all groups, activate htl10.py
activate_htl10()
