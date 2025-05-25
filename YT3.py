
# pip install google-genai

import os
import re
import mimetypes
import struct
from google import genai
from google.genai import types

TRANSCRIPT_DIR = "Vid/Transcription"
TTS_OUTPUT_DIR = "Vid/tts"
MODEL = "gemini-2.5-flash-preview-tts"

def save_binary_file(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(data)
    print(f"File saved to: {file_path}")

def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    params = parse_audio_mime_type(mime_type)
    bits_per_sample = params["bits_per_sample"]
    sample_rate = params["rate"]
    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size
    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF", chunk_size, b"WAVE", b"fmt ", 16,
        1, num_channels, sample_rate,
        byte_rate, block_align, bits_per_sample,
        b"data", data_size
    )
    return header + audio_data

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
        elif "audio/L" in param:
            try:
                bits_per_sample = int(param.split("L")[1])
            except:
                pass
    return {"bits_per_sample": bits_per_sample, "rate": rate}

def clean_transcription(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    cleaned_lines = []
    for line in lines:
        if re.match(r"\d+", line.strip()):
            continue  # skip [number] lines
        if re.match(r"\d{2}:\d{2}–\d{2}:\d{2}", line.strip()):
            continue  # skip timestamp lines
        cleaned_lines.append(line.strip())
    return " ".join(cleaned_lines).strip()

def generate_tts(text, file_stem):
    client = genai.Client(api_key=os.environ.get("GEMINI_API"))

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text)],
        ),
    ]

    config = types.GenerateContentConfig(
        temperature=1,
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name="Enceladus"
                )
            )
        ),
    )

    for chunk in client.models.generate_content_stream(
        model=MODEL, contents=contents, config=config
    ):
        if (
            chunk.candidates
            and chunk.candidates[0].content
            and chunk.candidates[0].content.parts
            and chunk.candidates[0].content.parts[0].inline_data
        ):
            inline_data = chunk.candidates[0].content.parts[0].inline_data
            audio_data = inline_data.data
            file_ext = mimetypes.guess_extension(inline_data.mime_type) or ".wav"
            if file_ext == ".bin":
                audio_data = convert_to_wav(audio_data, inline_data.mime_type)
                file_ext = ".wav"
            save_binary_file(os.path.join(TTS_OUTPUT_DIR, f"{file_stem}{file_ext}"), audio_data)

def main():
    os.makedirs(TTS_OUTPUT_DIR, exist_ok=True)
    for filename in os.listdir(TRANSCRIPT_DIR):
        if filename.endswith(".txt"):
            file_path = os.path.join(TRANSCRIPT_DIR, filename)
            print(f"Processing: {file_path}")
            text = clean_transcription(file_path)
            if text:
                file_stem = os.path.splitext(filename)[0]
                generate_tts(text, file_stem)
            else:
                print(f"Empty text after cleaning: {filename}")

if __name__ == "__main__":
    main()
