
# CHECK_HALAL.py

# To run this code, you need to install:
# pip install google-genai

import os
from google import genai
from google.genai import types

def check_halal_status():
    print("=== HALAL CHECK SCRIPT STARTED ===")

    # Load API key
    api_key = os.environ.get("GEMINI_API")
    if not api_key:
        print("❌ GEMINI_API environment variable is not set.")
        return
    print("✅ Loaded GEMINI_API key.")

    # Initialize client
    client = genai.Client(api_key=api_key)
    model = "gemini-2.5-flash-preview-04-17"
    print(f"✅ Initialized Google GenAI client with model: {model}")

    # Load transcript from file
    transcript_path = os.path.join("Vid", "Transcript.txt")
    if not os.path.exists(transcript_path):
        print(f"❌ Transcript file not found at: {transcript_path}")
        return

    print(f"📂 Loading transcript from: {transcript_path}")
    with open(transcript_path, 'r', encoding='utf-8') as f:
        transcript = f.read().strip()

    print("✅ Transcript loaded successfully.")
    
    # Construct the prompt
    prompt = (
        "From the above transcript is there any script that can be considered prohibited or haram in Islam? "
        "If so, only output its timeline. If not, just output the word 'HALAL'."
    )

    print("📝 Creating content for Gemini request...")
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=transcript),
                types.Part.from_text(text=prompt)
            ]
        )
    ]

    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    # Output file path
    output_path = "/home/runner/work/71/71/Vid/HALAL.txt"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print("🚀 Sending request to Gemini API...")
    try:
        with open(output_path, 'w', encoding='utf-8') as out:
            print("🔄 Awaiting response...\n")
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                if hasattr(chunk, "text"):
                    print(chunk.text, end="")  # Print to terminal
                    out.write(chunk.text)      # Write to file
                else:
                    print("⚠️ Unexpected chunk format:", chunk)

        print(f"\n\n✅ HALAL check completed and saved at: {os.path.abspath(output_path)}")

    except Exception as e:
        print(f"\n❌ Failed to check halal status or save output: {e}")

    print("=== SCRIPT FINISHED ===")

if __name__ == "__main__":
    check_halal_status()
