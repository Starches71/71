
import os
import google.generativeai as genai
from google.generativeai.types import Content, Part, FileData, GenerateContentConfig

def generate():
    # Configure the API key
    genai.configure(api_key=os.environ.get("GEMINI_API"))

    model = genai.GenerativeModel("gemini-2.5-flash-preview-04-17")

    contents = [
        Content(
            role="user",
            parts=[
                Part(
                    file_data=FileData(
                        file_uri="https://www.youtube.com/watch?v=K13qt-0dkk4",
                        mime_type="video/*",
                    )
                ),
                Part.from_text(
                    text="""
Watch this video carefully: https://www.youtube.com/watch?v=K13qt-0dkk4

Your task is to generate a professional YouTube voiceover script for this video, as if you're naturally narrating it to an audience.

--- Instructions:
Write in a clear, modern, and conversational tone that feels natural for a voice narrator. Break the voiceover into short segments with timestamps like this:
00:00–00:04

After each timestamp, write only the sentence to be spoken during that time. Every single scene in the video must have its own narration. Do not leave any part of the video without a corresponding spoken line.

If the video contains silent scenes or music only, use that time to describe what’s happening on screen in a compelling, story-driven way. Do not insert filler like “music playing” or “no audio.” Instead, express what the viewer sees or feels in those moments.

The narration should flow like a story and highlight key features naturally — not as a list. Avoid restating on-screen text directly. Instead, translate the visuals into value, emotion, or experience.

Follow the pacing of the video closely. Your lines should match the timing of the visuals.
"""
                ),
            ],
        )
    ]

    config = GenerateContentConfig(response_mime_type="text/plain")

    response = model.generate_content(contents=contents, generation_config=config)

    print(response.text)

if __name__ == "__main__":
    generate()
