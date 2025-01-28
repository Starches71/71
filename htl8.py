
import os
import subprocess

# Directory paths
input_dir = "best_vid"
output_dir = "best_vid_clean"

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Process each file in the input directory
for video_file in os.listdir(input_dir):
    if ".mp4" in video_file:  # Process files containing .mp4 in their names
        input_path = os.path.join(input_dir, video_file)

        # Remove audio
        silenced_video_path = os.path.join(output_dir, f"silenced_{video_file}")
            "ffmpeg", "-i", input_path, "-c", "copy", "-an", silenced_video_path,
            "-y"  # Overwrite if file exists
        ])

        # Split the silenced video into 5 parts
        for idx in range(5):
            start_time = idx * 10  # Calculate start time for each segment
            base_name = video_file.rsplit('.', 1)[0]  # Remove the file extension
            output_piece_name = f"{base_name}.{chr(97 + idx)}.mp4"  # Name: 2.B.a.mp4, 2.B.b.mp4, etc.
            output_piece_path = os.path.join(output_dir, output_piece_name)

                "ffmpeg", "-i", silenced_video_path, "-ss", f"{start_time}", "-t", "10",
                "-c", "copy", output_piece_path,
                "-y"  # Overwrite if file exists
            ])

        print(f"Processed: {video_file}")

# After processing, run htl9.py
