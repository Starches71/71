
import base64
import mimetypes
import os
import re
import struct
from google.generativeai import GenerativeModel, types

TRANSCRIPT_PATH = "/home/runner/work/71/71/Vid/Transcript.txt"
OUTPUT_FILE = "transcript_audio"

def save_binary_file(file_name, data):
    with open(file_name, "wb") as f:
        f.write(data)
    print(f"File saved to: {file_name}")

def clean_transcript(path):
    with open(path, "r") as f:
        lines = f.readlines()

    cleaned = []
    for line in lines:
        if re.fullmatch(r"\d+|\d{1,2}:\d{2}", line.strip()):
            continue
        cleaned_line = re.sub(r"\b\d{1,2}:\d{2}\b", "", line)
        cleaned_line = re.sub(r"\b\d+\b", "", cleaned_line)
        cleaned.append(cleaned_line.strip())

    return " ".join(filter(None, cleaned))

def generate():
    api_key = os.environ.get("GEMINI_API")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set in the environment")

    # Initialize the GenerativeModel with the API key
    model = GenerativeModel(model_name="gemini-2.5-flash-preview-tts", api_key=api_key)

    text_input = clean_transcript(TRANSCRIPT_PATH)

    contents = [types.Content(role="user", parts=[text_input])]

    generate_content_config = types.GenerationConfig(
        temperature=1,
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            voice=types.VoiceSelectionConfig(
                name="en-US-Standard-A"
            )
        ),
    )

    response = model.generate_content(
        contents=contents,
        generation_config=generate_content_config,
        stream=True,
    )

    for chunk in response:
        if not chunk.parts:
            continue

        part = chunk.parts[0]
        if hasattr(part, "inline_data") and part.inline_data:
            inline_data = part.inline_data
            data_buffer = base64.b64decode(inline_data.data)
            file_extension = mimetypes.guess_extension(inline_data.mime_type)

            if not file_extension:
                file_extension = ".wav"
                data_buffer = convert_to_wav(data_buffer, inline_data.mime_type or "audio/L16;rate=24000")

            save_binary_file(f"{OUTPUT_FILE}{file_extension}", data_buffer)
        elif hasattr(part, "text"):
            print(part.text)

def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    parameters = parse_audio_mime_type(mime_type)
    bits_per_sample = parameters["bits_per_sample"]
    sample_rate = parameters["rate"]
    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size
    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF", chunk_size, b"WAVE", b"fmt ", 16, 1,
        num_channels, sample_rate, byte_rate,
        block_align, bits_per_sample, b"data", data_size
    )
    return header + audio_data

def parse_audio_mime_type(mime_type: str) -> dict:
    bits_per_sample = 16
    rate = 24000
    if not mime_type:
        return {"bits_per_sample": bits_per_sample, "rate": rate}
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

if __name__ == "__main__":
    generate()
