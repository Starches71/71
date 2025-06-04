
import asyncio
import os
import re
from edge_tts import Communicate

# === Configuration ===
TRANSCRIPT_FILE = os.path.join("Vid", "Transcript.txt")
OUTPUT_DIR = "Vid"
VOICE_NAME = "en-US-SteffanNeural"
RETRIES = 3
RETRY_DELAY = 7  # seconds between retries
REQUEST_DELAY = 7  # seconds between each TTS call

# === Ensure output directory exists ===
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Filename sanitizer ===
def sanitize_filename(timeline):
    return timeline.replace("–", "-").replace(":", "_").strip()

# === Parse transcript blocks ===
def parse_transcript_blocks(text):
    text = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", text)
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

# === Generate TTS with retries ===
async def generate_tts_for_block(timeline, content, retries=RETRIES):
    filename = os.path.join(OUTPUT_DIR, f"{timeline}.mp3")
    if os.path.exists(filename):
        print(f"⏩ Skipping {timeline} (already exists)")
        return

    for attempt in range(1, retries + 1):
        try:
            print(f"🔊 [{attempt}/{retries}] Generating: {timeline}")
            tts = Communicate(text=content, voice=VOICE_NAME)
            await tts.save(filename)
            print(f"✅ Saved: {filename}")
            return
        except Exception as e:
            print(f"❌ Error on attempt {attempt} for {timeline}: {e}")
            await asyncio.sleep(RETRY_DELAY)

    print(f"🚫 Giving up on {timeline} after {retries} attempts")

# === Main entry point ===
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

    print(f"🧩 Found {len(blocks)} timeline blocks.")
    for timeline, content in blocks:
        await generate_tts_for_block(timeline, content)
        await asyncio.sleep(REQUEST_DELAY)  # delay between TTS requests

    print("\n✅ All timeline-based TTS files have been processed.")

# === Run the script ===
if __name__ == "__main__":
    asyncio.run(main())
