
import os
import mimetypes
import struct
import wave
from google import genai
from google.genai import types

def save_binary_file(file_name, data):
    with open(file_name, "wb") as f:
        f.write(data)
    print(f"[INFO] File saved to: {file_name}", flush=True)

def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    """Convert raw audio to .wav format."""
    params = parse_audio_mime_type(mime_type)
    bits_per_sample = params["bits_per_sample"]
    sample_rate = params["rate"]
    channels = 1
    byte_rate = sample_rate * channels * (bits_per_sample // 8)
    block_align = channels * (bits_per_sample // 8)
    data_size = len(audio_data)
    chunk_size = 36 + data_size

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF", chunk_size, b"WAVE", b"fmt ", 16,
        1,  # PCM
        channels,
        sample_rate,
        byte_rate,
        block_align,
        bits_per_sample,
        b"data", data_size
    )
    return header + audio_data

def parse_audio_mime_type(mime_type: str) -> dict[str, int | None]:
    """Extract bits_per_sample and sample rate from MIME type."""
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
    output_path = "/home/runner/work/71/71/Vid/tts.wav"

    # Load script
    print(f"[INFO] Loading script from: {script_path}", flush=True)
    with open(script_path, "r", encoding="utf-8") as f:
        script_text = f.read()

    # Set up genai client
    print("[INFO] Initializing Gemini TTS Client...", flush=True)
    genai_client = genai.Client(api_key=os.environ.get("GEMINI_API"))

    model = "gemini-2.5-flash-preview-tts"
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(script_text)],
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
    audio_chunks = b""
    mime_type = "audio/L16;rate=24000"  # default fallback
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
                audio_chunks += part.inline_data.data
                mime_type = part.inline_data.mime_type

    # Convert to WAV
    wav_data = convert_to_wav(audio_chunks, mime_type)
    save_binary_file(output_path, wav_data)

    # Verify audio duration
    print("[INFO] Verifying audio duration...", flush=True)
    try:
        with wave.open(output_path, "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration = frames / float(rate)
        print(f"[INFO] Audio duration: {duration:.2f} seconds", flush=True)
    except Exception as e:
        print(f"[ERROR] Could not determine duration: {e}", flush=True)

if __name__ == "__main__":
    generate()
