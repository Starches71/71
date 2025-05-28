
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
SCRIPT_PATH = "/home/runner/work/71/71/Vid/script.txt"
RAW_PATH = "/home/runner/work/71/71/Vid/tts.raw"
MP3_PATH = "/home/runner/work/71/71/Vid/tts.mp3"

# === Gemini API Key ===
API_KEY = os.getenv("GEMINI_API")

def save_binary_file(file_name, data):
    with open(file_name, "wb") as f:
        f.write(data)

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
            "-ar", "24000",
            "-ac", "1",
            out_file.name
        ]

        process = subprocess.run(cmd, capture_output=True)
        if process.returncode != 0:
            raise RuntimeError(process.stderr.decode())

        out_file.seek(0)
        return out_file.read()

def split_text(text, max_chars=8000):
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

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

    for part_text in text_parts:
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
            # === Print entire chunk directly from the API ===
            print(chunk)

            if chunk.candidates and chunk.candidates[0].content and chunk.candidates[0].content.parts:
                part = chunk.candidates[0].content.parts[0]
                if part.inline_data and part.inline_data.data:
                    raw_audio_data.append(part.inline_data.data)

        time.sleep(60)

    return raw_audio_data

def concatenate_and_convert(all_raw_data):
    full_raw = b''.join(all_raw_data)
    save_binary_file(RAW_PATH, full_raw)

    input_format = "s16le"
    mp3_data = convert_audio_with_ffmpeg(full_raw, input_format=input_format)
    save_binary_file(MP3_PATH, mp3_data)

def main():
    if not API_KEY:
        return

    if not os.path.exists(SCRIPT_PATH):
        return

    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        full_text = f.read()

    text_parts = split_text(full_text, max_chars=8000)
    all_raw_data = generate_tts(text_parts)
    concatenate_and_convert(all_raw_data)

if __name__ == "__main__":
    main()
