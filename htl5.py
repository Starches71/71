
import os
import asyncio
import edge_tts  # Make sure you have installed edge_tts
from pathlib import Path
import subprocess  # For running external scripts

# Directories
best_intro_dir = "best_intro"
best_outro_dir = "best_outro"
best_clean_dir = "best_clean"
best_audio_dir = "best_audio"

# Ensure the audio directory exists
os.makedirs(best_audio_dir, exist_ok=True)

# Function to process each file and convert it to speech asynchronously
async def process_text_to_speech(directory, prefix=""):
    # List all text files in the given directory
    files = os.listdir(directory)

    for file_name in files:
        # Get the full file path
        file_path = os.path.join(directory, file_name)

        # Read the content of the file
        with open(file_path, "r") as file:
            text = file.read().strip()  # Remove any leading/trailing whitespace

        # Clean up the text (strip any unwanted spaces)
        if directory == best_clean_dir:
            text = text.strip()  # This removes leading/trailing spaces

        # Prepare the filename for the MP3 file in the 'best_audio' directory
        mp3_filename = f"{prefix}{file_name}.mp3"
        mp3_path = os.path.join(best_audio_dir, mp3_filename)

        # Create the speech using the TTS library (using Andrew Neural US English voice)
        communicate = edge_tts.Communicate(text, voice="en-US-AndrewNeural")  # You can choose your voice here

        # Generate and save the MP3 file asynchronously
        await communicate.save(mp3_path)
        print(f"Generated speech for {file_name} and saved to {mp3_path}")

# Main function to handle the asynchronous processing
async def main():
    # Process best_intro and best_outro
    await process_text_to_speech(best_intro_dir, prefix="intro_")
    await process_text_to_speech(best_outro_dir, prefix="outro_")

    # Process best_clean
    await process_text_to_speech(best_clean_dir, prefix="")

    # Activate htl6.py after processing all files

# Run the main async function
if __name__ == "__main__":
    asyncio.run(main())
