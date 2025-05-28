import base64
import mimetypes
import os
import struct
import subprocess
import tempfile
import time
from google import genai
from google.genai import types

# === Configurable paths ===
SCRIPT_PATH = "/home/runner/work/71/71/Vid/script.txt"  # Input text
RAW_PATH = "/home/runner/work/71/71/Vid/tts.raw"         # Output raw audio
MP3_PATH = "/home/runner/work/71/71/Vid/tts.mp3"         # Output MP3 audio

# === Gemini API Key ===
API_KEY = os.getenv("GEMINI_API")

# === Save binary data to file ===
def save_binary_file(file_name, data):
    with open(file_name, "wb") as f:
        f.write(data)
    print(f"File saved to: {file_name}")

# === Convert raw audio data to MP3 using ffmpeg ===
def convert_audio_with_ffmpeg(input_data: bytes, input_format: str = None) -> bytes:
    with tempfile.NamedTemporaryFile(delete=True, suffix=".raw") as in_file, \
         tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as out_file:

        in_file.write(input_data)
        in_file.flush()

        input_format_option = ["-f", input_format] if input_format else []

        cmd = [
            "ffmpeg",
            "-y",
            *input_format_option,
            "-i", in_file.name,
            "-ar", "24000",     # Sample rate
            "-ac", "1",         # Mono
            out_file.name
        ]

        process = subprocess.run(cmd, capture_output=True)
        if process.returncode != 0:
            print("ffmpeg error:", process.stderr.decode())
            raise RuntimeError("ffmpeg conversion failed")

        out_file.seek(0)
        return out_file.read()

# === Split long text into smaller parts for Gemini ===
def split_text(text, max_chars=8000):
    parts = []
    while text:
        parts.append(text[:max_chars])
        text = text[max_chars:]
    return parts

# === Generate TTS using Gemini and return raw audio data ===
def generate_tts(text_parts):
    client = genai.Client(api_key=API_KEY)
    model = "gemini-2.5-flash-preview-tts"

    speaker_configs = [
        types.SpeakerVoiceConfig(
            speaker="Speaker 1",
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Enceladus")
            )
        )
    ]

    raw_audio_data = []

    for i, part_text in enumerate(text_parts):
        print(f"Processing chunk {i+1}/{len(text_parts)}...")

        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=part_text)],
            ),
        ]

        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            response_modalities=["audio"],
            speech_config=types.SpeechConfig(
                multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                    speaker_voice_configs=speaker_configs
                )
            ),
        )

        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            if (
                chunk.candidates is None
                or chunk.candidates[0].content is None
                or chunk.candidates[0].content.parts is None
            ):
                continue

            part = chunk.candidates[0].content.parts[0]

            if part.inline_data and part.inline_data.data:
                raw_data = part.inline_data.data
                raw_audio_data.append(raw_data)
            else:
                print("Text chunk received instead of audio:", chunk.text)

        print("Waiting 60 seconds to avoid rate limits...")
        time.sleep(60)

    return raw_audio_data

# === Concatenate and convert all raw audio chunks to MP3 ===
def concatenate_and_convert(all_raw_data):
    full_raw = b''.join(all_raw_data)
    save_binary_file(RAW_PATH, full_raw)

    input_format = "s16le"  # Signed 16-bit PCM little-endian
    mp3_data = convert_audio_with_ffmpeg(full_raw, input_format=input_format)
    save_binary_file(MP3_PATH, mp3_data)

# === Main function ===
def main():
    if not API_KEY:
        print("GEMINI_API environment variable not set.")
        return

    if not os.path.exists(SCRIPT_PATH):
        print(f"Input file not found: {SCRIPT_PATH}")
        return

    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        full_text = f.read()

    text_parts = split_text(full_text, max_chars=8000)
    all_raw_data = generate_tts(text_parts)
    concatenate_and_convert(all_raw_data)

# === Run ===
if __name__ == "__main__":
    main()
