
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

    # Construct prompt
    prompt = (
        f"Watch this video carefully: {yt_url} "
        "Your task is to generate a professional YouTube voiceover script for this video, as if you're naturally narrating it to an audience. "
        "--- Instructions: Write in a clear, modern, and conversational tone that feels natural for a voice narrator. "
        "Break the voiceover into short segments with timestamps like this: 00:00–00:04. "
        "After each timestamp, write only the sentence to be spoken during that time. "
        "Every single scene in the video must have its own narration. Do not leave any part of the video without a corresponding spoken line. "
        "If the video contains silent scenes or music only, use that time to describe what’s happening on screen in a compelling, story-driven way. "
        "Do not insert filler like 'music playing' or 'no audio.' Instead, express what the viewer sees or feels in those moments. "
        "The narration should flow like a story and highlight key features naturally — not as a list. "
        "Avoid restating on-screen text directly. Instead, translate the visuals into value, emotion, or experience. "
        "Follow the pacing of the video closely. Your lines should match the timing of the visuals. "
        "IMPORTANT: If the video contains speech in a language other than English, please translate and write the entire transcript in fluent English,make sure timeline format is like (00:00-00:20)."
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
    output_path = os.path.join("Vid", "Transcript.txt")

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

        # Confirm successful saving
        print(f"\n\nTranscript saved successfully at: {os.path.abspath(output_path)}")

    except Exception as e:
        print(f"\n\nFailed to generate or save transcript: {e}")

if __name__ == "__main__":
    generate()
