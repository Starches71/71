
import os
import re
import subprocess
from datetime import datetime
from google import genai
from google.genai import types

Constants

INPUT_FILE = "ASMR_SHORT.txt"
USED_FILE = "ASMR_USED.txt"
LINK_PATH = os.path.join("Vid", "yt_link")
FILTER_RESULT_PATH = os.path.join("Vid", "filter_result.txt")
MAX_ATTEMPTS = 31

def load_links():
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
lines = [line.strip() for line in f if line.strip()]
return [(lines[i], lines[i + 1]) for i in range(len(lines) - 1) if lines[i + 1].startswith("https://")]

def load_used_links():
if os.path.exists(USED_FILE):
with open(USED_FILE, 'r', encoding='utf-8') as f:
return set(line.strip() for line in f if line.strip())
return set()

def save_used_link(link):
with open(USED_FILE, 'a', encoding='utf-8') as f:
f.write(link + "\n")

def commit_changes(file_to_commit):
print("\n📦 Committing changes to GitHub...")
try:
subprocess.run(['git', 'config', '--global', 'user.name', 'yt-bot'], check=True)
subprocess.run(['git', 'config', '--global', 'user.email', 'yt-bot@example.com'], check=True)
subprocess.run(['git', 'stash', '--include-untracked'], check=True)
subprocess.run(['git', 'pull', '--rebase', 'origin', 'main'], check=True)
subprocess.run(['git', 'stash', 'pop'], check=True)
subprocess.run(['git', 'add', file_to_commit], check=True)

result = subprocess.run(['git', 'diff', '--cached', '--quiet'])  
    if result.returncode != 0:  
        msg = f"✅ Update {file_to_commit} - {datetime.utcnow().isoformat()}"  
        subprocess.run(['git', 'commit', '-m', msg], check=True)  
        subprocess.run(['git', 'push'], check=True)  
        print("✅ Changes committed and pushed.")  
    else:  
        print("ℹ️ No changes to commit.")  
except subprocess.CalledProcessError as e:  
    print(f"❌ Git commit failed: {e}")

def filter_link_with_gemini(yt_url):
try:
client = genai.Client(api_key=os.environ.get("GEMINI_API"))
model = "gemini-2.0-flash"
prompt = (
f"Watch this video: {yt_url} "
"Answer with a single word only: 'Yes' or 'No'. "
"Does the video contain any of the following: music (even background), female (voice or appearance), human face, or anything haram? "
"Also answer 'Yes' if it’s not an ASMR or product review video. "
"Answer 'No' only if it's strictly a product review or ASMR with no haram, no music, no face, no women. Just answer Yes or No."
)

contents = [  
        types.Content(  
            role="user",  
            parts=[  
                types.Part(file_data=types.FileData(file_uri=yt_url, mime_type="video/*")),  
                types.Part.from_text(text=prompt)  
            ],  
        )  
    ]  

    generate_content_config = types.GenerateContentConfig(response_mime_type="text/plain")  

    for chunk in client.models.generate_content_stream(  
        model=model,  
        contents=contents,  
        config=generate_content_config,  
    ):  
        response = chunk.text.strip().lower()  
        if response in ["yes", "no"]:  
            print(f"🔍 Gemini response: {response}")  
            with open(FILTER_RESULT_PATH, 'w', encoding='utf-8') as out:  
                out.write(response)  
            return response  
except Exception as e:  
    print(f"❌ Gemini API failed: {e}")  
return "yes"

def main():
os.makedirs("Vid", exist_ok=True)
all_links = load_links()
used_links = load_used_links()

fail_count = 0  
for info_line, link_line in all_links:  
    if link_line in used_links:  
        continue  

    # Save as used BEFORE processing  
    save_used_link(link_line)  
    print(f"\n🚀 Processing: {link_line}")  
    with open(LINK_PATH, 'w', encoding='utf-8') as f:  
        f.write(link_line)  

    result = filter_link_with_gemini(link_line)  

    if result == "no":  
        print("✅ Safe ASMR found. Halting process.")  
        commit_changes(USED_FILE)  
        return  
    else:  
        fail_count += 1  
        print(f"❌ Unsafe video ({fail_count} failed).")  

        if fail_count >= MAX_ATTEMPTS:  
            print("\n⚠️ 31 consecutive unsafe videos. Resting.")  
            commit_changes(USED_FILE)  
            return  

print("\n⚠️ All links used or filtered. Nothing clean found.")  
commit_changes(USED_FILE)

if name == "main":
main()
