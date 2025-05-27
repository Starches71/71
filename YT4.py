def generate():
    import os
    import mimetypes
    import wave
    import google.generativeai as genai
    from pydub import AudioSegment

    # Load script
    input_path = "/home/runner/work/71/71/Vid/script.txt"
    print(f"[INFO] Loading script from: {input_path}", flush=True)
    with open(input_path, "r", encoding="utf-8") as f:
        script_text = f.read()

    # Configure genai client
    print("[INFO] Initializing Gemini Client...", flush=True)
    genai.configure(api_key=os.environ.get("GEMINI_API"))

    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash-latest",
        generation_config={
            "temperature": 1,
        },
        system_instruction="You are a helpful assistant.",
        tools=[]
    )

    # Speech generation model (TTS)
    tts_model = genai.GenerativeModel(
        model_name="models/gemini-tts",
    )

    print("[INFO] Sending request to Gemini for TTS generation...", flush=True)
    response = tts_model.generate_content(
        contents=script_text,
        generation_config={
            "response_mime_type": "audio/wav",
        },
        voice="Enceladus"
    )

    file_name_base = "/home/runner/work/71/71/Vid/tts"
    final_path = f"{file_name_base}.wav"

    try:
        with open(final_path, "wb") as out_file:
            out_file.write(response._content)  # Raw audio bytes
        print(f"[INFO] Audio saved to: {final_path}", flush=True)
    except Exception as e:
        print(f"[ERROR] Failed to save audio: {e}", flush=True)
        return

    # Verify audio duration
    print("[INFO] Verifying audio duration...", flush=True)
    try:
        with wave.open(final_path, "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration = frames / float(rate)

        print(f"[INFO] Audio duration: {duration:.2f} seconds", flush=True)
    except Exception as e:
        print(f"[ERROR] Could not determine audio duration: {e}", flush=True)
