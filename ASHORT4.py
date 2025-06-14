
# product_check.py

# To run this code, you need to install:
# pip install google-genai

import os
from google import genai
from google.genai import types

def check_for_product_video():
    # Load API key and model
    client = genai.Client(api_key=os.environ.get("GEMINI_API"))
    model = "gemini-2.0-flash"

    # Load YouTube link
    link_path = os.path.join("Vid", "yt_link")
    with open(link_path, 'r') as f:
        yt_url = f.read().strip()

    # Updated prompt
    prompt = (
        f"Watch this video: {yt_url} "
        "Answer this question with a single word only: 'Yes' or 'No'. "
        "I'm looking for a product review, product showcase, or any real product video. "
        "Does the video show an actual product clearly and focus on reviewing or showcasing it? "
        "Only answer 'Yes' if it's clearly a real product video. No explanation."
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
    output_path = os.path.join("Vid", "product.txt")

    # Run generation and save result
    try:
        with open(output_path, 'w', encoding='utf-8') as out:
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                answer = chunk.text.strip()
                if answer.lower() in ["yes", "no"]:
                    print(f"Product Review Detected: {answer}")
                    out.write(answer)
                    break

        print(f"Saved result to: {os.path.abspath(output_path)}")

    except Exception as e:
        print(f"Failed to check for product video: {e}")


if __name__ == "__main__":
    check_for_product_video()
