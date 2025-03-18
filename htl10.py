
import os
import subprocess

# Directories
best_join = "best_join"
best_audio = "best_audio"
best_clip = "best_clip"

# Create output directory if it doesn't exist
os.makedirs(best_clip, exist_ok=True)
print(f"Directory '{best_clip}' is ready for output files.")

# Loop through video files in `best_join` directory
for video in os.listdir(best_join):
    if video.endswith(".mp4"):
        print(f"Processing video: {video}")
        
        # Extract number from video filename
        vid_num = os.path.splitext(video)[0]
        print(f"Extracted video number: {vid_num}")
        
        # Find corresponding audio file in `best_audio` directory
        audio_files = [f for f in os.listdir(best_audio) if f.startswith(vid_num)]
        
        if audio_files:
            audio_file = os.path.join(best_audio, audio_files[0])
            print(f"Matching audio file found: {audio_file}")
            
            # Output file name for combined video and audio
            output = os.path.join(best_clip, f"{vid_num}.mp4")
            print(f"Output file will be: {output}")
            
            # Combine video and audio
            try:
                subprocess.run(
                    [
                        "ffmpeg", "-i", os.path.join(best_join, video),
                        "-i", audio_file, "-c:v", "copy", "-c:a", "aac", "-strict", "-2", output
                    ],
                    check=True
                )
                print(f"Successfully combined video and audio for: {video}")
            except subprocess.CalledProcessError as e:
                print(f"Error combining {video} with {audio_file}: {e}")
        else:
            print(f"No matching audio file found for video: {video}")

print("\nAll processing completed successfully.")
