
import re
import os

# Define input/output paths
input_path = "/home/runner/work/71/71/Vid/Transcript.txt"
output_path = "/home/runner/work/71/71/Vid/script.txt"

print(f"[INFO] Loading transcript from: {input_path}")

# Check if input file exists
if not os.path.exists(input_path):
    print(f"[ERROR] Transcript file not found: {input_path}")
    exit(1)

# Regex to match timestamps (e.g., 00:20-00:40)
timestamp_pattern = re.compile(r"^\d{2}:\d{2}-\d{2}:\d{2}")

cleaned_lines = []

with open(input_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print(f"[INFO] Total lines in transcript: {len(lines)}")

    for i, line in enumerate(lines, 1):
        original_line = line.strip()
        if timestamp_pattern.match(original_line):
            # Remove timestamp and leading/trailing symbols
            cleaned_line = re.sub(timestamp_pattern, '', original_line).strip(" :-")
            if cleaned_line:
                cleaned_lines.append(cleaned_line)
                print(f"[MATCHED] Line {i}: {cleaned_line}")
            else:
                print(f"[SKIPPED] Line {i}: Empty after cleaning")
        else:
            print(f"[IGNORED] Line {i}: Doesn't match timestamp pattern")

# Join all cleaned lines into a single paragraph
final_script = ' '.join(cleaned_lines)

# Write output
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(final_script)

# Post-process report
print(f"\n[INFO] Cleaned script saved to: {output_path}")
if final_script.strip():
    print(f"[SUCCESS] Script contains {len(final_script.split())} words and {len(final_script)} characters.\n")
    print("[SCRIPT PREVIEW]")
    print("============================================")
    print(final_script)
    print("============================================")
else:
    print("[WARNING] Final script is empty. Nothing was matched or cleaned.")
