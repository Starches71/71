
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import os
import re

VIDEO_PATH = "Vid/blurred_output.mp4"
AUDIO_DIR = "Vid"

# Pattern to extract time from filename like 00_37-00_42.mp3
time_pattern = re.compile(r"(\d{2})_(\d{2})-(\d{2})_(\d{2})")

def time_to_seconds(hh, mm):
    return int(hh) * 60 + int(mm)

def parse_filename(filename):
    match = time_pattern.search(filename)
    if not match:
        return None
    start = time_to_seconds(match.group(1), match.group(2))
    end = time_to_seconds(match.group(3), match.group(4))
    return start, end

# Load video
video = VideoFileClip(VIDEO_PATH)
audio_clips = []

for file in os.listdir(AUDIO_DIR):
    if file.endswith(".mp3") and time_pattern.search(file):
        full_path = os.path.join(AUDIO_DIR, file)
        start_time, end_time = parse_filename(file)
        max_duration = end_time - start_time

        audio = AudioFileClip(full_path)
        # Trim if audio is longer than the target duration
        if audio.duration > max_duration:
            audio = audio.subclip(0, max_duration)

        # Shift audio to start time
        audio = audio.set_start(start_time)
        audio_clips.append(audio)

# Combine all audio overlays
final_audio = CompositeAudioClip(audio_clips)
# Set final audio to video
final_video = video.set_audio(final_audio)

# Export the final video
final_video.write_videofile("Vid/final_output.mp4", codec="libx264", audio_codec="aac")
