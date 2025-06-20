
# GEMINI.py

# To run this code, you need to install:
# pip install google-genai

import os
from google import genai
from google.genai import types

def generate():
    # Load API key
    client = genai.Client(api_key=os.environ.get("GEMINI_API"))
    model = "gemini-2.0-flash"

    # Load YouTube link from file
    link_path = os.path.join("Vid", "yt_link")
    with open(link_path, 'r') as f:
        yt_url = f.read().strip()

    # Prompt to extract product names
    prompt = (
        f"Watch this video: {yt_url}\n\n"
        "List the **name(s)** of any product being reviewed or shown in this video.\n"
        "Format your answer exactly like this:\n"
        "■Product 1\n■Product 2\n■Product 3\n\n"
        "If it's only one product, just return one line in the same format.\n"
        "Do not add any extra text or explanation — only the product names, each starting with '■'."
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
    output_path = os.path.join("Vid", "product_names.txt")

    # Run generation and save output
    try:
        with open(output_path, 'w', encoding='utf-8') as out:
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                clean_text = chunk.text.strip()
                if clean_text:
                    print("[✓] Extracted Product Names:\n", clean_text)
                    out.write(clean_text)
                    break  # Only need the first valid block

        print(f"\nSaved product names to: {os.path.abspath(output_path)}")

    except Exception as e:
        print(f"\n[✘] Failed to extract or save product names: {e}")

if __name__ == "__main__":
    generate()
