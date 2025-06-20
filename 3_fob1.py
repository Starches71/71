
# GEMINI_FILTER.py

import os
from google import genai
from google.genai import types

def analyze_video():
    # Load API key
    client = genai.Client(api_key=os.environ.get("GEMINI_API"))
    model = "gemini-2.0-flash"

    # Load YouTube link from file
    link_path = os.path.join("Vid", "yt_link")
    with open(link_path, 'r') as f:
        yt_url = f.read().strip()

    # Construct filtering prompt
    prompt = (
        f"Watch this video: {yt_url} "
        "Answer with a single word only: 'Yes' or 'No'. "
        "Does the video contain **any of the following**: "
        "music (even background), female (voice or appearance), any human face (even male), or anything considered haram? "
        "Also answer 'Yes' if it's NOT an ASMR or product review video. "
        "If it's strictly a product review or ASMR with no haram, music, faces, or women, then answer 'No'. "
        "Your response must be only 'Yes' or 'No'. No explanation."
    )

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part(
                    file_data=types.FileData(
                        file_uri=yt_url,
                        mime_type="video/*",
                    )
                ),
                types.Part.from_text(text=prompt)
            ],
        )
    ]

    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    os.makedirs("Vid", exist_ok=True)
    output_path = os.path.join("Vid", "filter_result.txt")

    try:
        with open(output_path, 'w', encoding='utf-8') as out:
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                clean_text = chunk.text.strip()
                if clean_text.lower() in ["yes", "no"]:
                    print(f"Answer: {clean_text}")
                    out.write(clean_text)
                    break  # Stop at first valid response

        print(f"\nSaved result to: {os.path.abspath(output_path)}")

    except Exception as e:
        print(f"\n❌ Failed to generate or save result: {e}")

if __name__ == "__main__":
    analyze_video()
