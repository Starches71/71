import os
import subprocess

# Directories
input_dir = "best_io"
output_dir = "best_io2"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)
print(f"Output directory '{output_dir}' is ready.")

# Function to remove silences from a video
def remove_silences(input_file, output_file):
    """Removes silences from the input video file and saves it to the output file."""
    print(f"Processing file to remove silences: {input_file}")
    command = [
        "ffmpeg", "-i", input_file,
        "-af", "silenceremove=start_periods=1:start_duration=0.5:start_threshold=-50dB",
        "-c:v", "copy", "-c:a", "aac", "-y", output_file
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Silences removed successfully. Saved to: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing file '{input_file}': {e}")

# Main function to process intro and outro files
def main():
    # List all files in input directory
    print(f"Scanning input directory: {input_dir}")
    files = os.listdir(input_dir)

    # Filter for intro and outro files
    intro_file = next((f for f in files if "intro" in f.lower()), None)
    outro_file = next((f for f in files if "outro" in f.lower()), None)

    if not intro_file and not outro_file:
        print("No intro or outro files found in the directory.")
        return

    # Process intro file
    if intro_file:
        input_path = os.path.join(input_dir, intro_file)
        output_path = os.path.join(output_dir, intro_file)
        remove_silences(input_path, output_path)

    # Process outro file
    if outro_file:
        input_path = os.path.join(input_dir, outro_file)
        output_path = os.path.join(output_dir, outro_file)
        remove_silences(input_path, output_path)

if __name__ == "__main__":
    main()
