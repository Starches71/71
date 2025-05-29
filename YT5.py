import os
import base64
import subprocess

def save_binary_file(file_name, data):
    with open(file_name, "wb") as f:
        f.write(data)
    print(f"[INFO] File saved to: {file_name}", flush=True)

def get_file_info(file_path):
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        with open(file_path, "rb") as f:
            header = f.read(10)
        print(f"[INFO] File: {file_path} | Size: {size} bytes | Header: {header.hex()}", flush=True)
    else:
        print(f"[WARN] File not found: {file_path}", flush=True)

def convert_raw_to_mp3(raw_path: str, mp3_path: str, sample_rate=24000, channels=1):
    print("[INFO] Checking RAW audio before conversion...", flush=True)
    get_file_info(raw_path)

    cmd = [
        "ffmpeg",
        "-v", "verbose",
        "-y",
        "-f", "s16le",  # Signed 16-bit little-endian PCM
        "-ar", str(sample_rate),
        "-ac", str(channels),
        "-i", raw_path,
        mp3_path
    ]
    print("[INFO] Converting RAW to MP3 via ffmpeg...", flush=True)
    result = subprocess.run(cmd, capture_output=True)
    print("[FFMPEG STDOUT]\n" + result.stdout.decode(), flush=True)
    print("[FFMPEG STDERR]\n" + result.stderr.decode(), flush=True)

    if result.returncode != 0:
        print(f"[ERROR] FFmpeg failed with return code {result.returncode}", flush=True)
    else:
        print(f"[INFO] MP3 saved to: {mp3_path}", flush=True)
        get_audio_duration(mp3_path)

def get_audio_duration(file_path):
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        duration = float(result.stdout.decode().strip())
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        print(f"[INFO] MP3 Duration: {duration:.2f} seconds ({minutes:02d}:{seconds:02d})", flush=True)
    except Exception as e:
        print(f"[ERROR] Failed to get duration: {e}", flush=True)

def main():
    # === Change these paths ===
    raw_path = "/home/runner/work/71/71/Vid/tts.raw"
    mp3_path = "/home/runner/work/71/71/Vid/tts.mp3"

    # If the binary is base64 encoded (as a string), decode it here:
    with open("binary_audio.txt", "r") as f:  # ← your base64 string file
        base64_data = f.read().strip()
    decoded_data = base64.b64decode(base64_data)

    save_binary_file(raw_path, decoded_data)
    convert_raw_to_mp3(raw_path, mp3_path)

if __name__ == "__main__":
    main()
