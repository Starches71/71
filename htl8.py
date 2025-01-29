import os
import subprocess
import time

# Directory paths
input_dir = "best_vid"
output_dir = "best_vid_clean"

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"📁 Created output directory: {output_dir}")

# Wait a few seconds to ensure all files from htl7.py are fully saved
print("⏳ Waiting 5 seconds to ensure all files exist...")
time.sleep(5)

# Get updated list of MP4 files
video_files = [f for f in os.listdir(input_dir) if f.endswith(".mp4")]
if not video_files:
    print(f"🚨 No .mp4 files found in {input_dir}")
    exit(1)
else:
    print(f"🎥 Found {len(video_files)} .mp4 files in '{input_dir}'")

# Process each video file
for video_file in video_files:
    print(f"\n📂 Processing file: {video_file}")

    input_path = os.path.join(input_dir, video_file)
    silenced_video_path = os.path.join(output_dir, f"silenced_{video_file}")

    # Step 1: Remove audio
    try:
        print(f"🔇 Removing audio from {video_file}...")
        subprocess.run(["ffmpeg", "-i", input_path, "-c", "copy", "-an", silenced_video_path, "-y"], check=True)
        print(f"✅ Audio removed: {silenced_video_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error removing audio from {video_file}: {e}")
        continue

    # Step 2: Split video into 5 parts
    print(f"✂️ Splitting silenced video into 5 parts...")
    for idx in range(5):
        start_time = idx * 10
        base_name = video_file.rsplit(".", 1)[0]
        output_piece_name = f"{base_name}.{chr(97 + idx)}.mp4"
        output_piece_path = os.path.join(output_dir, output_piece_name)

        try:
            print(f"🎬 Creating segment {chr(97 + idx)} at {start_time} seconds...")
            subprocess.run([
                "ffmpeg", "-i", silenced_video_path, "-ss", f"{start_time}", "-t", "10",
                "-c", "copy", output_piece_path, "-y"
            ], check=True)
            print(f"✅ Segment created: {output_piece_path}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating segment {chr(97 + idx)}: {e}")
            continue

    print(f"🏁 Finished processing: {video_file}")

print("\n✅ All files processed successfully.")

# Check if any missing files
processed_files = [f for f in os.listdir(output_dir) if f.endswith(".mp4")]
print(f"\n🔎 Final check: {len(processed_files)} files exist in '{output_dir}'.")

if len(processed_files) < len(video_files) * 5:
    print("⚠️ Some files may not have been processed. Check logs for errors!")
