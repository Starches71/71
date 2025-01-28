
import os
import subprocess

# Directory paths
input_dir = "best_vid"
output_dir = "best_vid_clean"

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created output directory: {output_dir}")
else:
    print(f"Output directory already exists: {output_dir}")

# Check if there are .mp4 files in the input directory
video_files = [f for f in os.listdir(input_dir) if f.endswith(".mp4")]
if not video_files:
    print(f"No .mp4 files found in directory: {input_dir}")
    exit(1)
else:
    print(f"Found {len(video_files)} .mp4 files in '{input_dir}'")

# Process each video file in the input directory
for video_file in video_files:
    print(f"\nProcessing file: {video_file}")

    input_path = os.path.join(input_dir, video_file)

    # Step 1: Remove audio
    silenced_video_path = os.path.join(output_dir, f"silenced_{video_file}")
    try:
        print(f"Removing audio from {video_file}...")
        subprocess.run([
            "ffmpeg", "-i", input_path, "-c", "copy", "-an", silenced_video_path, "-y"  # Overwrite if file exists
        ], check=True)
        print(f"Audio removed. Saved silenced video as: {silenced_video_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error removing audio from {video_file}: {e}")
        continue

    # Step 2: Split the silenced video into 5 parts
    print(f"Splitting silenced video into 5 parts...")
    for idx in range(5):
        start_time = idx * 10  # Calculate start time for each segment
        base_name = video_file.rsplit('.', 1)[0]  # Remove the file extension
        output_piece_name = f"{base_name}.{chr(97 + idx)}.mp4"  # e.g., 2.B.a.mp4, 2.B.b.mp4, etc.
        output_piece_path = os.path.join(output_dir, output_piece_name)

        try:
            print(f"Creating segment {chr(97 + idx)} starting at {start_time} seconds...")
            subprocess.run([
                "ffmpeg", "-i", silenced_video_path, "-ss", f"{start_time}", "-t", "10",
                "-c", "copy", output_piece_path, "-y"  # Overwrite if file exists
            ], check=True)
            print(f"Segment {chr(97 + idx)} created: {output_piece_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error creating segment {chr(97 + idx)} for {video_file}: {e}")
            continue

    print(f"Finished processing: {video_file}")

print("\nAll files processed successfully.")
