
import os
import base64
import struct
import subprocess
from google import genai
from google.genai import types

def save_binary_file(file_name, data: bytes):
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

def get_audio_duration(file_path):
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries",
             "format=duration", "-of",
             "default=noprint_wrappers=1:nokey=1", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        duration = float(result.stdout.decode().strip())
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        print(f"[INFO] MP3 Duration: {duration:.2f} seconds ({minutes:02d}:{seconds:02d})", flush=True)
    except Exception as e:
        print(f"[ERROR] Failed to get duration: {e}", flush=True)

def convert_raw_to_mp3(raw_path: str, mp3_path: str, sample_rate=24000, channels=1):
    print("[INFO] Analyzing RAW audio before conversion...", flush=True)
    get_file_info(raw_path)

    cmd = [
        "ffmpeg",
        "-y",
        "-f", "s16le",
        "-ar", str(sample_rate),
        "-ac", str(channels),
        "-i", raw_path,
        mp3_path
    ]
    print("[INFO] Converting RAW to MP3 via ffmpeg...", flush=True)
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print(f"[ERROR] FFmpeg failed:\n{result.stderr.decode()}", flush=True)
    else:
        print(f"[INFO] MP3 saved to: {mp3_path}", flush=True)
        verify_mp3(mp3_path)
        get_audio_duration(mp3_path)

def verify_mp3(mp3_path):
    if not os.path.exists(mp3_path):
        print(f"[ERROR] MP3 file was not created.", flush=True)
        return
    try:
        with open(mp3_path, "rb") as f:
            header = f.read(3)
        if header == b'ID3' or header[:2] == b'\xff\xfb':
            print("[SUCCESS] Output file is a valid MP3 format ✅", flush=True)
        else:
            print(f"[WARN] Output file might not be a valid MP3 (Header: {header.hex()})", flush=True)
    except Exception as e:
        print(f"[ERROR] Couldn't verify MP3 file: {e}", flush=True)

def parse_audio_mime_type(mime_type: str) -> dict[str, int | None]:
    bits_per_sample = 16
    rate = 24000
    parts = mime_type.split(";")
    for param in parts:
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate = int(param.split("=")[1])
            except:
                pass
        elif param.startswith("audio/L"):
            try:
                bits_per_sample = int(param.split("L")[1])
            except:
                pass
    return {"bits_per_sample": bits_per_sample, "rate": rate}

def generate():
    script_path = "/home/runner/work/71/71/Vid/script.txt"
    raw_path = "/home/runner/work/71/71/Vid/tts.raw"
    mp3_path = "/home/runner/work/71/71/Vid/tts.mp3"

    print(f"[INFO] Loading script from: {script_path}", flush=True)
    with open(script_path, "r", encoding="utf-8") as f:
        script_text = f.read()

    print("[INFO] Initializing Gemini TTS Client...", flush=True)
    genai_client = genai.Client(api_key=os.environ.get("GEMINI_API"))

    model = "gemini-2.5-flash-preview-tts"
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=script_text)],
        )
    ]
    config = types.GenerateContentConfig(
        temperature=1,
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Enceladus")
            )
        ),
    )

    print("[INFO] Sending TTS request via streaming...", flush=True)
    audio_bytes = b""
    mime_type = "audio/L16;rate=24000"

    for chunk in genai_client.models.generate_content_stream(
        model=model, contents=contents, config=config
    ):
        if (
            chunk.candidates
            and chunk.candidates[0].content
            and chunk.candidates[0].content.parts
        ):
            part = chunk.candidates[0].content.parts[0]
            if part.inline_data and part.inline_data.data:
                # DECODE BASE64
                audio_bytes += base64.b64decode(part.inline_data.data)
                mime_type = part.inline_data.mime_type

    # Save decoded binary audio
    save_binary_file(raw_path, audio_bytes)

    print(f"[INFO] Detected MIME type: {mime_type}", flush=True)

    params = parse_audio_mime_type(mime_type)
    convert_raw_to_mp3(raw_path, mp3_path, sample_rate=params["rate"], channels=1)

if __name__ == "__main__":
    generate()
