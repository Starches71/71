
import os
import subprocess

# Directories
audio_dir = "best_audio"
video_dir = "best_vid_clean"
output_dir = "best_io"

# Intro and Outro audio files
intro_audio = "intro_best_intro.txt.mp3"
outro_audio = "outro_best_outro.txt.mp3"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)
print(f"Output directory '{output_dir}' is ready.")

def get_audio_duration(file_path):
    """Get the duration of an audio file using ffprobe."""
    print(f"Getting duration for audio file: {file_path}")
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        duration = float(result.stdout.strip())
        print(f"Duration of '{file_path}': {duration} seconds")
        return duration
    except subprocess.CalledProcessError as e:
        print(f"Error getting duration for {file_path}: {e}")
        return 0.0

def combine_videos_with_audio(audio_file, output_file):
    """Combine videos with an audio file, trimming to fit."""
    print(f"Combining videos with audio file: {audio_file}")
    audio_path = os.path.join(audio_dir, audio_file)
    output_path = os.path.join(output_dir, output_file)

    # Get audio duration
    audio_duration = get_audio_duration(audio_path)
    if audio_duration == 0.0:
        print(f"Skipping {audio_file} due to invalid duration.")
        return

    video_duration = 10  # Assume each video segment is 10 seconds long
    temp_video_list = "temp_videos.txt"

    total_duration = 0.0
    with open(temp_video_list, "w") as temp_file:
        print("Creating temporary video list...")
        for video in sorted(os.listdir(video_dir)):
            if video.endswith("A.a.mp4"):
                video_path = os.path.join(video_dir, video)
                temp_file.write(f"file '{video_path}'\n")
                total_duration += video_duration
                print(f"Added video: {video}, total duration: {total_duration} seconds")
                if total_duration >= audio_duration:
                    print("Reached audio duration limit. Stopping.")
                    break

    # Combine videos into a single file
    print("Combining videos into 'temp_combined.mp4'...")
    try:
        subprocess.run(
            ["ffmpeg", "-f", "concat", "-safe", "0", "-i", temp_video_list, "-c", "copy", "temp_combined.mp4", "-y"],
            check=True
        )
        print("Temporary combined video created: 'temp_combined.mp4'")
    except subprocess.CalledProcessError as e:
        print(f"Error combining videos: {e}")
        return

    # Trim the combined video to match the audio duration
    print(f"Trimming video to match audio duration. Saving as: {output_path}")
    try:
        subprocess.run(
            [
                "ffmpeg", "-i", "temp_combined.mp4", "-i", audio_path,
                "-c:v", "copy", "-c:a", "aac", "-shortest", output_path, "-y"
            ],
            check=True
        )
        print(f"Final video created: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error trimming video: {e}")

    # Clean up temporary files
    print("Cleaning up temporary files...")
    os.remove("temp_combined.mp4")
    os.remove(temp_video_list)
    print("Temporary files removed.")

# Combine intro and outro videos with their respective audio files
print("Processing intro video...")
combine_videos_with_audio(intro_audio, "intro_best_intro.mp4")

print("Processing outro video...")
combine_videos_with_audio(outro_audio, "outro_best_outro.mp4")

print("All tasks completed.")
