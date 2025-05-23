
import os
import google.generativeai as genai

def main():
    api_key = os.getenv("GEMINI_API")
    if not api_key:
        raise ValueError("GEMINI_API environment variable is not set")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = """Watch this https://www.youtube.com/watch?v=K13qt-0dkk4

Your task is to generate a professional YouTube voiceover script for this video, as if you're naturally narrating it to an audience.

Instructions:
- Write in a clear, modern, and conversational tone that feels natural for a voice narrator.
- Break the voiceover into short segments with timestamps like this:   `00:00–00:04`
- After each timestamp, write only the sentence to be spoken during that time.
- If the video contains silent scenes or music only, use that time to describe what's happening on screen in a compelling, story-driven way. Do not insert filler like “hey” or “music.” Instead, say what the viewer would be seeing or feeling.
- The narration should flow like a story and highlight key features naturally.
- Do not include commentary, formatting notes, tags, or explanations. Only return the final spoken lines with their exact time windows.
- Follow the pacing of the video closely based on both visuals and timing. You are allowed to interpret the visuals and create narration that would match the look and feel of the scenes, even if there’s no dialogue.
"""

    response = model.generate_content(prompt)
    print(response.text)

if __name__ == "__main__":
    main()
