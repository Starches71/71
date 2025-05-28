
import os
import subprocess
import time
from google import genai
from google.genai import types

def save_binary_file(file_name: str, data: bytes) -> None:
    with open(file_name, "wb") as f:
        f.write(data)
    print(f"[INFO] File saved to: {file_name} (size: {len(data)} bytes)", flush=True)

def get_file_info(file_path: str) -> None:
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        with open(file_path, "rb") as f:
            header = f.read(10)
        print(f"[INFO] File: {file_path} | Size: {size} bytes | Header: {header.hex()}", flush=True)
    else:
        print(f"[WARN] File not found: {file_path}", flush=True)

def convert_raw_to_mp3(raw_path: str, mp3_path: str, sample_rate: int = 24000, channels: int = 1) -> None:
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
    print("[INFO] Running ffmpeg command:", " ".join(cmd), flush=True)
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print(f"[ERROR] FFmpeg failed:\n{result.stderr.decode()}", flush=True)
    else:
        print(f"[INFO] MP3 saved to: {mp3_path}", flush=True)
        verify_mp3(mp3_path)

def verify_mp3(mp3_path: str) -> None:
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

def parse_audio_mime_type(mime_type: str) -> dict[str, int]:
    bits_per_sample = 16
    rate = 24000
    parts = mime_type.split(";")
    for param in parts:
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate = int(param.split("=")[1])
            except ValueError:
                pass
        elif "audio/L" in param:
            try:
                bits_per_sample = int(param.split("L")[1])
            except ValueError:
                pass
    return {"bits_per_sample": bits_per_sample, "rate": rate}

def split_script(text: str, max_tokens: int = 8000) -> list[str]:
    print("[INFO] Splitting script into parts...", flush=True)
    approx_token_len = lambda t: int(len(t) / 4)
    parts = []
    start = 0
    while start < len(text):
        end = start + max_tokens * 4
        parts.append(text[start:end])
        start = end
    print(f"[INFO] Total parts created: {len(parts)}", flush=True)
    return parts

def generate():
    script_path = "/home/runner/work/71/71/Vid/script.txt"
    raw_path = "/home/runner/work/71/71/Vid/tts.raw"
    mp3_path = "/home/runner/work/71/71/Vid/tts.mp3"

    print(f"[INFO] Loading script from: {script_path}", flush=True)
    with open(script_path, "r", encoding="utf-8") as f:
        script_text = f.read()

    print("[INFO] Initializing Gemini TTS Client...", flush=True)
    genai_client = genai.Client(api_key=os.environ.get("GEMINI_API"))

    model = "models/gemini-2.5-flash-preview-tts"
    config_base = types.GenerateContentConfig(
        temperature=1,
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt=types.PrebuiltVoice(voice="Enceladus")
            )
        ),
    )

    script_parts = split_script(script_text, max_tokens=8000)
    audio_chunks = b""
    mime_type = "audio/L16;rate=24000"

    for i, part_text in enumerate(script_parts):
        print(f"\n[INFO] >>> Processing part {i+1}/{len(script_parts)}", flush=True)
        contents = [types.Content(role="user", parts=[types.Part.from_text(text=part_text)])]

        print("[INFO] Sending TTS request to Gemini...", flush=True)
        chunk_data = b""
        chunk_count = 0

        try:
            stream = genai_client.generate_content_stream(
                model=model,
                contents=contents,
                generation_config=config_base
            )
            for chunk in stream:
                chunk_count += 1
                if chunk.candidates and chunk.candidates[0].content and chunk.candidates[0].content.parts:
                    part = chunk.candidates[0].content.parts[0]
                    if part.inline_data and part.inline_data.data:
                        data_piece = part.inline_data.data
                        chunk_data += data_piece
                        print(f"[DEBUG] Chunk {chunk_count}: {len(data_piece)} bytes", flush=True)
                        mime_type = part.inline_data.mime_type
        except Exception as e:
            print(f"[ERROR] Exception while calling Gemini TTS: {e}", flush=True)
            continue

        print(f"[INFO] Received {chunk_count} audio chunks totaling {len(chunk_data)} bytes", flush=True)
        audio_chunks += chunk_data

        if i < len(script_parts) - 1:
            print("[INFO] Waiting 60 seconds to avoid hitting limits...", flush=True)
            time.sleep(60)

    print(f"\n[INFO] Total combined audio length: {len(audio_chunks)} bytes", flush=True)
    print(f"[INFO] Detected final MIME type: {mime_type}", flush=True)

    save_binary_file(raw_path, audio_chunks)

    params = parse_audio_mime_type(mime_type)
    convert_raw_to_mp3(raw_path, mp3_path, sample_rate=params["rate"], channels=1)

if __name__ == "__main__":
    generate()
