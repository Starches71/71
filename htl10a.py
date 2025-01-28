
import os
import subprocess

# Directories
input_dir = "best_io"
output_dir = "best_io2"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)
print(f"Output directory '{output_dir}' is ready.")

# Function to remove silences from a video
def remove_silences(input_file, output_file):
    """
    Removes silences from the given input video file and saves the result to the output file.
    """
    print(f"Removing silences from file: {input_file}")
    command = [
        "ffmpeg", "-i", input_file,
        "-af", "silenceremove=1:0:-30dB",  # Adjust the threshold here as needed
        "-c:v", "copy", "-c:a", "aac", "-y", output_file
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Silences removed and saved to: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing file '{input_file}': {e}")

# Main function to process intro and outro files
def main():
    print("Starting the processing of intro and outro files...")

    # List all files in the input directory
    if not os.path.exists(input_dir):
        print(f"Input directory '{input_dir}' does not exist.")
        return

    files = os.listdir(input_dir)
    print(f"Files found in input directory '{input_dir}': {files}")

    # Filter for intro and outro files
    intro_file = next((f for f in files if "intro" in f.lower()), None)
    outro_file = next((f for f in files if "outro" in f.lower()), None)

    if not intro_file and not outro_file:
        print("No intro or outro files found in the directory.")
        return

    # Process intro file
    if intro_file:
        print(f"Intro file found: {intro_file}")
        input_path = os.path.join(input_dir, intro_file)
        output_path = os.path.join(output_dir, intro_file)
        remove_silences(input_path, output_path)
    else:
        print("No intro file found.")

    # Process outro file
    if outro_file:
        print(f"Outro file found: {outro_file}")
        input_path = os.path.join(input_dir, outro_file)
        output_path = os.path.join(output_dir, outro_file)
        remove_silences(input_path, output_path)
    else:
        print("No outro file found.")

    print("Processing of intro and outro files completed.")

# Entry point of the script
if __name__ == "__main__":
    main()
