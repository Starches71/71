
import base64
import mimetypes
import os
import re
import struct
from google import genai
from google.genai import types

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
    text_input = clean_transcript(TRANSCRIPT_PATH)

    # -------------------- FIX 1: Configure the client properly --------------------
    api_key = os.environ.get("GEMINI_API")  # <- CHANGED from GEMINI_API_KEY
    if not api_key:
        raise ValueError("GEMINI_API is not set in environment variables")
    genai.configure(api_key=api_key)  # <- NEW: correctly configures client
    # ------------------------------------------------------------------------------

    # -------------------- FIX 2: Proper model usage --------------------
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-preview-tts",
        generation_config={"response_mime_type": "audio/wav"},
        system_instruction="You are a narrator. Only read what is given, nothing more.",
    )
    # -------------------------------------------------------------------

    response = model.generate_content(
        text_input,
        generation_config=types.GenerationConfig(
            temperature=1,
            response_mime_type="audio/wav",
        ),
        safety_settings=None,
        stream=True,
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice=types.PrebuiltVoice(
                    name="Enceladus"  # <- Fixed voice name (as per official)
                )
            )
        ),
    )

    for chunk in response:
        if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
            continue

        part = chunk.candidates[0].content.parts[0]
        if hasattr(part, "inline_data") and part.inline_data:
            inline_data = part.inline_data
            data_buffer = inline_data.data
            file_extension = mimetypes.guess_extension(inline_data.mime_type)

            if not file_extension:
                file_extension = ".wav"
                data_buffer = convert_to_wav(data_buffer, inline_data.mime_type or "audio/L16;rate=24000")

            save_binary_file(f"{OUTPUT_FILE}{file_extension}", data_buffer)
        elif hasattr(chunk, "text"):
            print(chunk.text)

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
