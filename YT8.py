
# GEMINI_DESCRIPTION.py

# To run this code, you need to install:
# pip install google-genai

import os
from google import genai
from google.genai import types

def generate():
    # Load API key
    client = genai.Client(api_key=os.environ.get("GEMINI_API"))
    model = "gemini-2.5-flash-preview-04-17"

    # Load YouTube link from file
    link_path = os.path.join("Vid", "yt_link")
    with open(link_path, 'r') as f:
        yt_url = f.read().strip()

    # Simple prompt
    prompt = (
        f"Watch this video: {yt_url} "
        "Write a short, SEO-rich YouTube video description with relevant hashtags."
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

    # Ensure Vid directory exists
    os.makedirs("Vid", exist_ok=True)

    # Output file path
    output_path = os.path.join("Vid", "Description.txt")

    # Run generation and save output
    try:
        with open(output_path, 'w', encoding='utf-8') as out:
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                print(chunk.text, end="")
                out.write(chunk.text)

        print(f"\n\nDescription saved successfully at: {os.path.abspath(output_path)}")

    except Exception as e:
        print(f"\n\nFailed to generate or save description: {e}")

if __name__ == "__main__":
    generate()
