
import os
import subprocess

# Define directories
input_dir_io = "best_io3"
input_dir_clip = "best_clip3"
output_dir = "best_final"
final_output = os.path.join(output_dir, "final_output.mp4")

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)
print(f"Output directory '{output_dir}' is ready.")

# Check if input directories exist
if not os.path.exists(input_dir_io):
    print(f"Error: Input directory '{input_dir_io}' is missing.")
    exit(1)

if not os.path.exists(input_dir_clip):
    print(f"Error: Input directory '{input_dir_clip}' is missing.")
    exit(1)

print("Input directories validated.")

# Define video join order
join_order = [
    os.path.join(input_dir_io, "intro_best_intro.mp4"),
    os.path.join(input_dir_clip, "7.mp4"),
    os.path.join(input_dir_clip, "6.mp4"),
    os.path.join(input_dir_clip, "5.mp4"),
    os.path.join(input_dir_clip, "4.mp4"),
    os.path.join(input_dir_clip, "3.mp4"),
    os.path.join(input_dir_clip, "2.mp4"),
    os.path.join(input_dir_clip, "1.mp4"),
    os.path.join(input_dir_io, "outro_best_outro.mp4")
]

# Check for missing files
missing_files = [file for file in join_order if not os.path.exists(file)]
if missing_files:
    print("Error: The following files are missing:")
    for file in missing_files:
        print(f"  - {file}")
    exit(1)

print("All required video files are present.")

# Generate a temporary file list for ffmpeg
file_list = os.path.join(output_dir, "file_list.txt")
with open(file_list, "w") as f:
    for file in join_order:
        # Write absolute paths to avoid issues with ffmpeg
        f.write(f"file '{os.path.abspath(file)}'\n")
        
print(f"Temporary file list for ffmpeg created at {file_list}.")

# Use ffmpeg to concatenate the videos without re-encoding
ffmpeg_cmd = [
    "ffmpeg", "-f", "concat", "-safe", "0",
    "-i", file_list, "-c", "copy", final_output
]

try:
    subprocess.run(ffmpeg_cmd, check=True)
    print(f"Final video saved at {final_output}")
except subprocess.CalledProcessError as e:
    print("Error during video concatenation:", e)
    exit(1)

print("Video concatenation completed successfully.")
