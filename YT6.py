
import os
import re
import subprocess

VIDEO_PATH = "Vid/blurred_output.mp4"
AUDIO_DIR = "Vid"
OUTPUT_PATH = "Vid/final_output.mp4"

# Regex to extract time segments like 00_09-00_18
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

# Generate complex filter for FFmpeg
filter_complex = []
input_args = ['-i', VIDEO_PATH]  # first input: video
index = 1  # input index counter (video is 0)

for file in sorted(os.listdir(AUDIO_DIR)):
    if file.endswith('.mp3') and time_pattern.search(file):
        full_path = os.path.join(AUDIO_DIR, file)
        start, end = parse_filename(file)
        duration = end - start

        input_args += ['-i', full_path]
        filter_complex.append(
            f"[{index}:a]atrim=duration={duration},adelay={start * 1000}|{start * 1000}[a{index}]"
        )
        index += 1

# Combine all delayed audio tracks
if index == 1:
    print("❌ No audio files found.")
    exit(1)

# Join all audio overlays together
overlay = ''.join(f"[a{i}]" for i in range(1, index))
filter_complex.append(f"{overlay}amix=inputs={index-1}[mixed]")

# Final FFmpeg command
ffmpeg_command = [
    'ffmpeg',
    *input_args,
    '-filter_complex', ';'.join(filter_complex),
    '-map', '0:v',
    '-map', '[mixed]',
    '-c:v', 'libx264',
    '-c:a', 'aac',
    '-shortest',
    OUTPUT_PATH
]

# Run it
subprocess.run(ffmpeg_command)
