
import os
import subprocess
                                        # Directories
best_join = "best_join"
best_audio = "best_audio"               best_clip = "best_clip"
htl10a_script = "htl10a.py"             
# Create output directory if it doesn't exist                                   os.makedirs(best_clip, exist_ok=True)

# Loop through video files in `best_join` directory
for video in os.listdir(best_join):
    if video.endswith(".mp4"):
        # Extract number from video filename
        vid_num = os.path.splitext(video)[0]

        # Find corresponding audio file in `best_audio` directory
        audio_files = [f for f in os.listdir(best_audio) if f.startswith(vid_num)]
        if audio_files:
            audio_file = os.path.join(best_audio, audio_files[0])

            # Output file name for combined video and audio
            output = os.path.join(best_clip, f"{vid_num}.mp4")

            # Combine video and audio
            try:
                    "ffmpeg", "-i", os.path.join(best_join, video),
                    "-i", audio_file, "-c:v", "copy", "-c:a", "aac", "-strict", "-2", output
                ], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error combining {video} with {audio_file}: {e}")
                continue

# Activate `htl10a.py` script after all processing
try:
    print(f"Successfully activated {htl10a_script}.")
except subprocess.CalledProcessError as e:
    print(f"Error running {htl10a_script}: {e}")
