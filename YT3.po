
import re
import os

# Verbose mode toggle
VERBOSE = True

# Define paths
input_path = "/home/runner/work/71/71/Vid/Transcript.txt"
output_path = "/home/runner/work/71/71/Vid/script.txt"

print(f"[INFO] Loading transcript from: {input_path}")

if not os.path.exists(input_path):
    print(f"[ERROR] Transcript file not found: {input_path}")
    exit(1)

# Regex to match lines like 00:41-00:48 or 01:14-01-23
timestamp_pattern = re.compile(r"^\d{2}:\d{2}-\d{2}[:\-]\d{2}")

# Common LLM intro phrases
ignore_prefixes = [
    "here is the script",
    "here's your script",
    "sure! here's",
    "below is the script",
    "your script is",
    "transcript:"
]

def is_llm_intro(line):
    lower = line.lower().strip(": ").strip()
    return any(lower.startswith(prefix) for prefix in ignore_prefixes)

cleaned_lines = []

with open(input_path, 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

# Check and skip the first line if it's a likely LLM intro
if lines and is_llm_intro(lines[0]):
    if VERBOSE:
        print(f"[REMOVED] Line 1: LLM intro detected → \"{lines[0]}\"")
    lines = lines[1:]

i = 0
while i < len(lines):
    line = lines[i]

    if timestamp_pattern.match(line):
        if VERBOSE:
            print(f"[TIMESTAMP] Line {i+1}: {line}")
        i += 1
        if i < len(lines):
            text_line = lines[i]
            cleaned_lines.append(text_line)
            if VERBOSE:
                print(f"[ADDED] Line {i+1}: {text_line}")
    else:
        if VERBOSE:
            print(f"[SKIPPED] Line {i+1}: Not a timestamp → \"{line}\"")
    i += 1

# Join all text lines into one paragraph
final_script = ' '.join(cleaned_lines)

# Save to file
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(final_script)

print(f"\n[INFO] Cleaned script saved to: {output_path}")
if final_script.strip():
    print(f"[SUCCESS] Script contains {len(final_script.split())} words and {len(final_script)} characters.\n")
    print("[SCRIPT PREVIEW]")
    print("============================================")
    print(final_script)
    print("============================================")
else:
    print("[WARNING] Final script is empty. Nothing was matched or cleaned.")
