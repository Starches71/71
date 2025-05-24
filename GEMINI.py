
# GEMINI.py

# To run this code, you need to install:
# pip install google-genai

import os
from google import genai
from google.genai import types

def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API"),
    )

    model = "gemini-2.5-flash-preview-04-17"

    prompt = (
        "Watch this video carefully: https://www.youtube.com/watch?v=K13qt-0dkk4 "
        "Your task is to generate a professional YouTube voiceover script for this video, as if you're naturally narrating it to an audience. "
        "--- Instructions: Write in a clear, modern, and conversational tone that feels natural for a voice narrator. "
        "Break the voiceover into short segments with timestamps like this: 00:00–00:04 "
        "After each timestamp, write only the sentence to be spoken during that time. "
        "Every single scene in the video must have its own narration. Do not leave any part of the video without a corresponding spoken line. "
        "If the video contains silent scenes or music only, use that time to describe what’s happening on screen in a compelling, story-driven way. "
        "Do not insert filler like 'music playing' or 'no audio.' Instead, express what the viewer sees or feels in those moments. "
        "The narration should flow like a story and highlight key features naturally — not as a list. "
        "Avoid restating on-screen text directly. Instead, translate the visuals into value, emotion, or experience. "
        "Follow the pacing of the video closely. Your lines should match the timing of the visuals."
    )

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part(
                    file_data=types.FileData(
                        file_uri="https://youtu.be/K13qt-0dkk4",
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

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()
