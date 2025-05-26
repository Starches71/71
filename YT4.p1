
# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import mimetypes
import os
import re
import struct
from google import genai
from google.genai import types


def save_binary_file(file_name, data):
    with open(file_name, "wb") as f:
        f.write(data)
    print(f"[INFO] File successfully saved to: {file_name}")


def generate():
    input_path = "/home/runner/work/71/71/Vid/script.txt"
    print(f"[INFO] Loading script from: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        script_text = f.read()

    print("[INFO] Initializing Gemini Client...")
    client = genai.Client(api_key=os.environ.get("GEMINI_API"))

    model = "gemini-2.5-flash-preview-tts"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=script_text),
            ],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
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

    print("[INFO] Sending request to Gemini for TTS generation...")
    try:
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            print("[INFO] Chunk received from Gemini...")

            if (
                chunk.candidates is None
                or chunk.candidates[0].content is None
                or chunk.candidates[0].content.parts is None
            ):
                print("[WARNING] Chunk has no valid audio content. Skipping.")
                continue

            part = chunk.candidates[0].content.parts[0]
            if part.inline_data:
                inline_data = part.inline_data
                data_buffer = inline_data.data
                mime_type = inline_data.mime_type

                file_extension = mimetypes.guess_extension(mime_type)
                if file_extension is None:
                    print(f"[INFO] Unknown file extension for MIME type: {mime_type}. Converting to WAV.")
                    file_extension = ".wav"
                    data_buffer = convert_to_wav(data_buffer, mime_type)
                else:
                    print(f"[INFO] Detected file extension: {file_extension}")

                file_path = f"/home/runner/work/71/71/Vid/tts{file_extension}"
                save_binary_file(file_path, data_buffer)
                print("[SUCCESS] TTS audio generated and saved.")
            else:
                print("[INFO] No inline_data present in the chunk part. Possibly text output.")
                print("[DEBUG] Gemini text response:", chunk.text)
    except Exception as e:
        print(f"[ERROR] An error occurred while generating TTS: {e}")


def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    print("[INFO] Converting raw audio to WAV format...")
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
        b"RIFF",
        chunk_size,
        b"WAVE",
        b"fmt ",
        16,
        1,
        num_channels,
        sample_rate,
        byte_rate,
        block_align,
        bits_per_sample,
        b"data",
        data_size,
    )
    print("[INFO] WAV header constructed.")
    return header + audio_data


def parse_audio_mime_type(mime_type: str) -> dict[str, int | None]:
    print(f"[INFO] Parsing audio MIME type: {mime_type}")
    bits_per_sample = 16
    rate = 24000

    parts = mime_type.split(";")
    for param in parts:
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate = int(param.split("=")[1])
                print(f"[INFO] Extracted sample rate: {rate}")
            except Exception:
                print("[WARNING] Could not parse sample rate from MIME type.")
        elif param.startswith("audio/L"):
            try:
                bits_per_sample = int(param.split("L", 1)[1])
                print(f"[INFO] Extracted bits per sample: {bits_per_sample}")
            except Exception:
                print("[WARNING] Could not parse bits per sample from MIME type.")

    return {"bits_per_sample": bits_per_sample, "rate": rate}


if __name__ == "__main__":
    generate()
