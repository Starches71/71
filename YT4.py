import base64
import mimetypes
import os
import struct
import subprocess
from google import genai
from google.genai import types

# Load API key from environment variable
API_KEY = os.getenv("GEMINI_API")

# Define paths
script_path = "/home/runner/work/71/71/Vid/script.txt"
raw_path = "/home/runner/work/71/71/Vid/tts.raw"
mp3_path = "/home/runner/work/71/71/Vid/tts.wav"

def save_binary_file(file_name, data):
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, "wb") as f:
        f.write(data)
    print(f"File saved to: {file_name}")

def convert_audio_with_ffmpeg(input_data: bytes, input_format: str = None) -> bytes:
    import tempfile

    with tempfile.NamedTemporaryFile(delete=True, suffix=".raw") as in_file, tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as out_file:
        in_file.write(input_data)
        in_file.flush()

        input_format_option = []
        if input_format:
            input_format_option = ["-f", input_format]

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
            print("ffmpeg error:", process.stderr.decode())
            raise RuntimeError("ffmpeg conversion failed")

        out_file.seek(0)
        return out_file.read()

def generate():
    if not API_KEY:
        raise EnvironmentError("GEMINI_API is not set in environment variables.")

    if not os.path.isfile(script_path):
        raise FileNotFoundError(f"Script file not found: {script_path}")

    with open(script_path, "r", encoding="utf-8") as f:
        script_text = f.read()

    client = genai.Client(api_key=API_KEY)

    model = "gemini-2.5-flash-preview-tts"
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=script_text)],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                speaker_voice_configs=[
                    types.SpeakerVoiceConfig(
                        speaker="Speaker 1",
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Zephyr")
                        ),
                    ),
                    types.SpeakerVoiceConfig(
                        speaker="Speaker 2",
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Puck")
                        ),
                    ),
                ]
            ),
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
            save_binary_file(raw_path, raw_data)

            input_format = None
            if part.inline_data.mime_type and "L16" in part.inline_data.mime_type:
                input_format = "s16le"

            try:
                wav_data = convert_audio_with_ffmpeg(raw_data, input_format)
                save_binary_file(mp3_path, wav_data)
            except Exception as e:
                print(f"Conversion failed: {e}")
        else:
            print(chunk.text)

if __name__ == "__main__":
    generate()
