
def generate():
    import os
    import mimetypes
    import wave
    from google.generativeai import Client, types
    from pydub import AudioSegment

    # Load script
    input_path = "/home/runner/work/71/71/Vid/script.txt"
    print(f"[INFO] Loading script from: {input_path}", flush=True)
    with open(input_path, "r", encoding="utf-8") as f:
        script_text = f.read()

    print("[INFO] Initializing Gemini Client...", flush=True)
    client = Client(api_key=os.environ.get("GEMINI_API"))

    model = "gemini-2.5-flash-preview-tts"
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=script_text)],
        )
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

    print("[INFO] Sending request to Gemini for TTS generation...", flush=True)
    file_name_base = "/home/runner/work/71/71/Vid/tts"

    audio_saved = False
    final_path = ""

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print("[INFO] Chunk received from Gemini...", flush=True)

        if not chunk.candidates:
            print("[WARNING] No candidates in chunk.", flush=True)
            continue

        candidate = chunk.candidates[0]
        content = candidate.content

        if not content or not content.parts:
            print("[WARNING] No parts found in content.", flush=True)
            continue

        part = content.parts[0]

        # Print raw text if returned
        if hasattr(part, "text") and part.text:
            print(f"[INFO] Gemini responded with text (not audio):\n{part.text.strip()}", flush=True)

        elif hasattr(part, "inline_data") and part.inline_data:
            print("[INFO] Valid audio data received.", flush=True)
            inline_data = part.inline_data
            data_buffer = inline_data.data
            file_extension = mimetypes.guess_extension(inline_data.mime_type) or ".wav"
            final_path = f"{file_name_base}{file_extension}"
            with open(final_path, "wb") as f:
                f.write(data_buffer)
            print(f"[INFO] Audio saved to: {final_path}", flush=True)
            audio_saved = True
        else:
            print("[WARNING] Chunk has no recognizable audio or text format.", flush=True)

    if not audio_saved:
        print("[ERROR] No audio file was saved. Nothing to analyze.", flush=True)
        return

    # Print audio duration
    print("[INFO] Verifying audio duration...", flush=True)
    try:
        if final_path.endswith(".wav"):
            with wave.open(final_path, "rb") as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                duration = frames / float(rate)
        else:
            audio = AudioSegment.from_file(final_path)
            duration = len(audio) / 1000.0

        print(f"[INFO] Audio duration: {duration:.2f} seconds", flush=True)
    except Exception as e:
        print(f"[ERROR] Could not determine audio duration: {e}", flush=True)
