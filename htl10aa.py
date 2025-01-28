import os
import subprocess

# Define directories
input_dir = "best_clip"
output_dir = "best_clip2"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)
print(f"Output directory '{output_dir}' is ready.")

# Iterate through all .mp4 files in the input directory
if not os.path.exists(input_dir):
    print(f"Input directory '{input_dir}' does not exist.")
else:
    files = os.listdir(input_dir)
    print(f"Files found in input directory '{input_dir}': {files}")

    for filename in files:
        if filename.endswith(".mp4"):
            print(f"Processing file: {filename}")
            
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            # Command to remove silence from video
            command = [
                "ffmpeg",
                "-i", input_path,
                "-af", "silenceremove=start_periods=1:start_duration=0.5:start_threshold=-30dB",
                output_path
            ]

            # Execute the command
            try:
                subprocess.run(command, check=True)
                print(f"Silences removed and saved to: {output_path}")
            except subprocess.CalledProcessError as e:
                print(f"Error processing file '{filename}': {e}")

print("Processing of all files completed.")
