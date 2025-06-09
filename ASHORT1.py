
# GEMINI.py

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

    # Prompt to check if the video is reviewing any haram product
    prompt = (
        f"Watch this video carefully: {yt_url} "
        "Answer this question with just one word: 'Yes' or 'No'. "
        "Is this video reviewing or promoting any product or service that is haram in Islam? "
        "Examples include products like pork, alcohol, gambling, interest-based financial services, un-Islamic cosmetics, or anything forbidden in Shariah. "
        "Only respond with 'Yes' or 'No'. No explanations or other text."
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
    output_path = os.path.join("Vid", "haram.txt")

    # Run generation and save output
    try:
        with open(output_path, 'w', encoding='utf-8') as out:
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                clean_text = chunk.text.strip()
                if clean_text.lower() in ["yes", "no"]:
                    print(f"Haram Product Detected: {clean_text}")
                    out.write(clean_text)
                    break  # Only need the first valid answer

        print(f"\nSaved answer to: {os.path.abspath(output_path)}")

    except Exception as e:
        print(f"\nFailed to generate or save answer: {e}")

if __name__ == "__main__":
    generate()
