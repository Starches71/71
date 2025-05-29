
import re
import os

# Path to the input transcript
input_path = "/home/runner/work/71/71/Vid/Transcript.txt"
output_path = "/home/runner/work/71/71/Vid/script.txt"

# Regex pattern to match timestamps (e.g., 00:20-00:40)
timestamp_pattern = re.compile(r"\d{2}:\d{2}-\d{2}:\d{2}")

cleaned_lines = []

with open(input_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if timestamp_pattern.match(line):
            # Only keep lines that start with a timestamp
            # Remove the timestamp itself
            line = re.sub(timestamp_pattern, '', line).strip(" :-")
            if line:
                cleaned_lines.append(line)

# Join all valid lines into a single paragraph
final_script = ' '.join(cleaned_lines)

# Write to output file
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(final_script)

# Print the path of the saved script
print(f"Cleaned script saved to: {output_path}")
