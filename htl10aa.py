import os
import subprocess                       
# Define directories                    input_dir = "best_clip"
output_dir = "best_clip2"
                                        # Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)  
# Iterate through all .mp4 files in the input directory
for filename in os.listdir(input_dir):      if filename.endswith(".mp4"):
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
        print(f"Processed: {filename}")

# Activate htl10b.py
print("Activating htl10b.py...")
