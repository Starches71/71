
# GEMINI.py

# To run this code, install:
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

    # Construct prompt for logical chapters (not fixed intervals)
    prompt = (
        f"Watch this video carefully: {yt_url}\n\n"
        "Your task is to divide the video into logical chapters based on content. Each chapter should represent a shift in topic, scene, or focus.\n\n"
        "Format:\n"
        "00:00–01:15 – [Chapter Title]\n"
        "01:15–02:30 – [Next Chapter Title]\n"
        "... and so on.\n\n"
        "--- Instructions ---\n"
        "• The timestamp range should match when that subtopic or scene starts and ends.\n"
        "• Chapter titles should be concise, meaningful, and reflect what the viewer experiences.\n"
        "• Do not create fixed time intervals — base each chapter on content.\n"
        "• Cover the entire video without skipping any parts.\n"
        "• Avoid repeating on-screen text; interpret the visuals and narration instead.\n"
        "• If there are silent or musical sections, describe what's visually happening.\n\n"
        "Output only the list of chapters in the format: START–END – Chapter Title"
    )

    # Save prompt (optional, for reference)
    os.makedirs("Vid", exist_ok=True)
    with open(os.path.join("Vid", "PromptUsed.txt"), 'w', encoding='utf-8') as pf:
        pf.write(prompt)

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

    # Save output to Chapters.txt
    output_path = os.path.join("Vid", "Chapters.txt")

    try:
        with open(output_path, 'w', encoding='utf-8') as out:
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                print(chunk.text, end="")
                out.write(chunk.text)

        print(f"\n\nChapters saved successfully at: {os.path.abspath(output_path)}")

    except Exception as e:
        print(f"\n\nFailed to generate or save chapters: {e}")

if __name__ == "__main__":
    generate()
