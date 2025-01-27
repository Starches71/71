
import os
import subprocess                       
# Directories
input_dir = "best_io"
output_dir = "best_io2"
htl11_script = "htl11b.py"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to remove silences from a video                                      def remove_silences(input_file, output_file):                                       # FFmpeg command to remove silence
    command = [
        "ffmpeg", "-i", input_file,
        "-af", "silenceremove=1:0:-50dB",
        "-c:v", "copy", "-c:a", "aac", "-y", output_file
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Silences removed: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing {input_file}: {e}")

# Main function to process intro and outro files
def main():
    # List all files in input directory
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

    # Activate htl11b.py after processing
    try:
        subprocess.run(["python3", htl11_script], check=True)
        print(f"Successfully activated {htl11_script}.")
    except subprocess.CalledProcessError as e:
        print(f"Error running {htl11_script}: {e}")

if __name__ == "__main__":
    main()
