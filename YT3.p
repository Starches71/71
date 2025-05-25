
# pip install google-genai

import os
import re
import mimetypes
import struct
from google import genai
from google.genai import types

TRANSCRIPT_DIR = "Vid/Transcript"
TTS_OUTPUT_DIR = "Vid/tts"
MODEL = "gemini-2.5-flash-preview-tts"


def save_binary_file(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(data)
    print(f"File saved: {file_path}")


def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    params = parse_audio_mime_type(mime_type)
    bits_per_sample = params["bits_per_sample"]
    sample_rate = params["rate"]
    num_channels = 1
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    data_size = len(audio_data)
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
    for param in mime_type.split(";"):
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


def clean_transcription(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.match(r"^\d+$", line):
            continue
        if re.match(r"^\d{2}:\d{2}[–-]\d{2}:\d{2}:", line):
            line = line.split(":", 1)[1].strip()
        cleaned_lines.append(line)
    return " ".join(cleaned_lines).strip()


def generate_tts(text: str, file_stem: str):
    api_key = os.environ.get("GEMINI_API")
    if not api_key:
        raise EnvironmentError("GEMINI_API environment variable not set.")

    client = genai.Client(api_key=api_key)

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

    try:
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
                safe_filename = re.sub(r"[^\w\-_.]", "_", file_stem)
                output_path = os.path.join(TTS_OUTPUT_DIR, f"{safe_filename}{file_ext}")
                save_binary_file(output_path, audio_data)
    except Exception as e:
        print(f"Error generating TTS for {file_stem}: {e}")


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
                print(f"Empty after cleaning: {filename}")


if __name__ == "__main__":
    main()
