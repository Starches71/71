
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import re
import os
import sys

VID_DIR = "Vid"
YT_LINK_FILE = os.path.join(VID_DIR, "yt_link")
TRANSCRIPT_FILE = os.path.join(VID_DIR, "transcript")

def extract_video_id(url_or_id):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url_or_id)
    if match:
        return match.group(1)
    elif len(url_or_id) == 11:
        return url_or_id
    else:
        print("Could not extract video ID.")
        sys.exit(1)

def merge_transcript_to_sentences(transcript):
    sentences = []
    current_sentence = ""
    start_time = None
    end_time = None
    sentence_end_re = re.compile(r'[.!?]')

    for entry in transcript:
        text = entry['text'].replace('\n', ' ').strip()
        if not text:
            continue

        if start_time is None:
            start_time = entry['start']

        current_sentence += (" " if current_sentence else "") + text
        end_time = entry['start'] + entry['duration']

        if sentence_end_re.search(current_sentence[-1]):
            sentences.append({
                "start": start_time,
                "end": end_time,
                "text": current_sentence.strip()
            })
            current_sentence = ""
            start_time = None
            end_time = None

    if current_sentence:
        sentences.append({
            "start": start_time,
            "end": end_time,
            "text": current_sentence.strip()
        })

    return sentences

def fetch_transcript(video_id):
    try:
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)

        try:
            return transcripts.find_manually_created_transcript(['en']).fetch()
        except:
            pass

        for t in transcripts:
            if not t.is_generated and t.is_translatable:
                try:
                    return t.translate('en').fetch()
                except:
                    continue

        try:
            return transcripts.find_generated_transcript(['en']).fetch()
        except:
            pass

        for t in transcripts:
            if t.is_generated and t.is_translatable:
                try:
                    return t.translate('en').fetch()
                except:
                    continue

        return None
    except (TranscriptsDisabled, NoTranscriptFound):
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def main():
    if not os.path.exists(YT_LINK_FILE):
        print("No yt_link file found.")
        sys.exit(1)

    with open(YT_LINK_FILE, 'r') as f:
        yt_url = f.read().strip()

    video_id = extract_video_id(yt_url)
    transcript = fetch_transcript(video_id)

    if not transcript:
        print("Transcript not found. Mark and rerun.")
        sys.exit(101)  # Special code to indicate "no transcript"

    sentences = merge_transcript_to_sentences(transcript)
    with open(TRANSCRIPT_FILE, 'w', encoding='utf-8') as f:
        for s in sentences:
            f.write(f"{s['start']:.2f} --> {s['end']:.2f}: {s['text']}\n")

    print("Transcript saved successfully.")

if __name__ == "__main__":
    main()
