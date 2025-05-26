
import os
from pydub import AudioSegment

def check_audio_duration():
    directory = "/home/runner/work/71/71/Vid"
    base_name = "tts"

    print("[INFO] Searching for audio file...", flush=True)

    # Find matching audio file
    audio_file = None
    for file in os.listdir(directory):
        if file.startswith(base_name) and file.lower().endswith((".mp3", ".wav", ".flac", ".ogg", ".m4a")):
            audio_file = os.path.join(directory, file)
            break

    if not audio_file:
        print("[ERROR] No audio file found with name starting 'tts' in the specified directory.", flush=True)
        return

    if os.path.getsize(audio_file) == 0:
        print(f"[ERROR] Audio file '{audio_file}' is empty.", flush=True)
        return

    try:
        audio = AudioSegment.from_file(audio_file)
        duration_sec = len(audio) / 1000.0
        print(f"[INFO] Found audio file: {audio_file}", flush=True)
        print(f"[INFO] Duration: {duration_sec:.2f} seconds", flush=True)
    except Exception as e:
        print(f"[ERROR] Could not load audio file '{audio_file}': {e}", flush=True)

# Run the function
check_audio_duration()
