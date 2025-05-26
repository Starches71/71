
def generate():
    import os
    import mimetypes
    from google.generativeai import Client, types

    # Load script
    input_path = "/home/runner/work/71/71/Vid/script.txt"
    print(f"[INFO] Loading script from: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        script_text = f.read()

    print("[INFO] Initializing Gemini Client...")
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

    print("[INFO] Sending request to Gemini for TTS generation...")
    file_name_base = "/home/runner/work/71/71/Vid/tts"

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print("[INFO] Chunk received from Gemini...")

        if not chunk.candidates:
            print("[WARNING] No candidates in chunk.")
            continue

        candidate = chunk.candidates[0]
        content = candidate.content

        if not content or not content.parts:
            print("[WARNING] No parts found in content.")
            continue

        part = content.parts[0]

        # Print raw text if returned
        if hasattr(part, "text") and part.text:
            print(f"[INFO] Gemini responded with text (not audio):\n{part.text.strip()}")

        # Handle valid audio
        elif hasattr(part, "inline_data") and part.inline_data:
            print("[INFO] Valid audio data received.")
            inline_data = part.inline_data
            data_buffer = inline_data.data
            file_extension = mimetypes.guess_extension(inline_data.mime_type)
            if not file_extension:
                print(f"[WARNING] Unknown MIME type: {inline_data.mime_type}. Defaulting to .wav")
                file_extension = ".wav"
                # Optionally convert format if needed

            output_path = f"{file_name_base}{file_extension}"
            with open(output_path, "wb") as f:
                f.write(data_buffer)
            print(f"[INFO] Audio saved to: {output_path}")
        else:
            print("[WARNING] Chunk has no recognizable audio or text format.")
