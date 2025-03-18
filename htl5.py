
import os
import asyncio
import edge_tts  # Make sure you have installed edge_tts
from pathlib import Path

# Directories
best_intro_dir = "best_intro"
best_outro_dir = "best_outro"
best_clean_dir = "best_clean"
best_audio_dir = "best_audio"

# Ensure the audio directory exists
os.makedirs(best_audio_dir, exist_ok=True)
print(f"Ensured that the directory '{best_audio_dir}' exists or was created.")

# Function to process each file and convert it to speech asynchronously
async def process_text_to_speech(directory, prefix=""):
    # List all text files in the given directory
    try:
        files = os.listdir(directory)
        print(f"Found {len(files)} files in the directory '{directory}'.")
    except Exception as e:
        print(f"Error listing files in directory '{directory}': {e}")
        return

    for file_name in files:
        # Get the full file path
        file_path = os.path.join(directory, file_name)

        # Read the content of the file
        try:
            with open(file_path, "r") as file:
                text = file.read().strip()  # Remove any leading/trailing whitespace
            print(f"Read content from file: {file_name}")
        except Exception as e:
            print(f"Error reading file '{file_name}': {e}")
            continue

        # Clean up the text (strip any unwanted spaces)
        if directory == best_clean_dir:
            text = text.strip()  # This removes leading/trailing spaces

        # Prepare the filename for the MP3 file in the 'best_audio' directory
        mp3_filename = f"{prefix}{file_name}.mp3"
        mp3_path = os.path.join(best_audio_dir, mp3_filename)

        # Create the speech using the TTS library (using Andrew Neural US English voice)
        try:
            communicate = edge_tts.Communicate(text, voice="en-US-AndrewNeural")  # You can choose your voice here
            # Generate and save the MP3 file asynchronously
            await communicate.save(mp3_path)
            print(f"Generated speech for {file_name} and saved to {mp3_path}")
        except Exception as e:
            print(f"Error generating speech for file '{file_name}': {e}")

# Main function to handle the asynchronous processing
async def main():
    # Process best_intro and best_outro
    print("Starting to process intro files...")
    await process_text_to_speech(best_intro_dir, prefix="intro_")
    
    print("Starting to process outro files...")
    await process_text_to_speech(best_outro_dir, prefix="outro_")

    # Process best_clean
    print("Starting to process cleaned content files...")
    await process_text_to_speech(best_clean_dir, prefix="")

# Run the main async function
if __name__ == "__main__":
    asyncio.run(main())
