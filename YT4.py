
import asyncio
import os
import re
from edge_tts import Communicate

# Directory where transcript and mp3s will be stored
TRANSCRIPT_FILE = os.path.join("Vid", "Transcript.txt")
OUTPUT_DIR = "Vid"

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Voice name
VOICE_NAME = "en-US-SteffanNeural"

# Function to sanitize filenames
def sanitize_filename(timeline):
    return timeline.replace("–", "-").replace(":", "_").strip()

# Flexible function to parse timeline blocks from transcript
def parse_transcript_blocks(text):
    # Fix cases like 'intofluentEnglish' → 'into fluent English'
    text = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", text)

    # Flexible regex pattern
    pattern = r"(?m)^(?:\d+\s+)?(?P<start>\d{2}:\d{2})\s*[-–]\s*(?P<end>\d{2}:\d{2})[:\-]?\s*(?P<content>.*?)\s*(?=^\d{2}:\d{2}\s*[-–]|^\Z|\n\d+\s+\d{2}:\d{2}\s*[-–])"

    matches = re.finditer(pattern, text, re.DOTALL | re.MULTILINE)

    blocks = []
    for match in matches:
        start = match.group("start")
        end = match.group("end")
        content = match.group("content").replace("\n", " ").strip()
        timeline = f"{start}-{end}".replace(":", "_")
        blocks.append((timeline, content))

    return blocks

# TTS function per block
async def generate_tts_for_block(timeline, content):
    filename = os.path.join(OUTPUT_DIR, f"{timeline}.mp3")
    print(f"🔊 Generating TTS for {timeline}...")
    try:
        tts = Communicate(text=content, voice=VOICE_NAME)
        await tts.save(filename)
        print(f"✅ Saved: {filename}")
    except Exception as e:
        print(f"❌ Error generating TTS for {timeline}: {e}")

# Main function
async def main():
    if not os.path.exists(TRANSCRIPT_FILE):
        print(f"❌ Transcript file not found: {TRANSCRIPT_FILE}")
        return

    with open(TRANSCRIPT_FILE, "r", encoding="utf-8") as file:
        transcript = file.read().strip()

    blocks = parse_transcript_blocks(transcript)

    if not blocks:
        print("❌ No valid timeline blocks found.")
        return

    for timeline, content in blocks:
        await generate_tts_for_block(timeline, content)

    print("\n✅ All timeline-based TTS files have been generated.")

# Run the script
if __name__ == "__main__":
    asyncio.run(main())
