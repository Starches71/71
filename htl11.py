
import os                               import subprocess                                                               # Directories                           audio_dir = "best_audio"
video_dir = "best_vid_clean"
output_dir = "best_io"                  
# Intro and Outro audio files
intro_audio = "intro_best_intro.txt.mp3"outro_audio = "outro_best_outro.txt.mp3"
                                        # Ensure output directory exists                                                os.makedirs(output_dir, exist_ok=True)
                                        def get_audio_duration(file_path):
    """Get the duration of an audio file using ffprobe."""
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return float(result.stdout.strip())

def combine_videos_with_audio(audio_file, output_file):
    """Combine videos with an audio file, trimming to fit."""
    audio_path = os.path.join(audio_dir, audio_file)
    output_path = os.path.join(output_dir, output_file)
    audio_duration = get_audio_duration(audio_path)
    video_duration = 10  # Assume each video segment is 10 seconds long
    temp_video_list = "temp_videos.txt"

    total_duration = 0.0
    with open(temp_video_list, "w") as temp_file:
        # Add video files to the temporary list
        for video in sorted(os.listdir(video_dir)):
            if video.endswith("A.a.mp4"):
                video_path = os.path.join(video_dir, video)
                temp_file.write(f"file '{video_path}'\n")
                total_duration += video_duration
                if total_duration >= audio_duration:
                    break

    # Combine videos
        ["ffmpeg", "-f", "concat", "-safe", "0", "-i", temp_video_list, "-c", "copy", "temp_combined.mp4", "-y"],
        check=True
    )

    # Trim the combined video to match the audio duration
        [
            "ffmpeg", "-i", "temp_combined.mp4", "-i", audio_path,
            "-c:v", "copy", "-c:a", "aac", "-shortest", output_path, "-y"
        ],
        check=True
    )

    # Clean up temporary files
    os.remove("temp_combined.mp4")
    os.remove(temp_video_list)

# Combine intro and outro
combine_videos_with_audio(intro_audio, "intro_best_intro.mp4")
combine_videos_with_audio(outro_audio, "outro_best_outro.mp4")

# Run htl11a.py
