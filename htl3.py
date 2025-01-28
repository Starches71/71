
import os
import subprocess

places_dir = "places"  # Path to the places directory
best_intro_dir = "best_intro"  # Path to the best_intro directory
best_outro_dir = "best_outro"  # Path to the best_outro directory

def main():
    print("Starting the process...")

    # Ensure directories exist
    try:
        os.makedirs(best_intro_dir, exist_ok=True)
        os.makedirs(best_outro_dir, exist_ok=True)
        print(f"Directories '{best_intro_dir}' and '{best_outro_dir}' created or already exist.")
    except Exception as e:
        print(f"Error creating directories: {e}")
        return

    # List all files in the places directory
    try:
        places = os.listdir(places_dir)
        print(f"Files in the places directory: {places}")
    except Exception as e:
        print(f"Error listing files in the '{places_dir}' directory: {e}")
        return

    # Check if there are any files in the places directory
    if places:
        # Get the first file in the list of places
        first_file = places[0]
        print(f"Processing the first file: {first_file}")

        try:
            # Open the first file and read its contents
            with open(os.path.join(places_dir, first_file), "r") as file:
                place = file.readline().strip()  # Read the first line and remove any extra spaces or newlines
            print(f"Place found: {place}")
        except Exception as e:
            print(f"Error reading the file '{first_file}': {e}")
            return

        # Define the content for best_intro and best_outro, replacing {place}
        best_intro_content = f"""Looking for the best places to stay in {place}? I’ve carefully handpicked the top hotels based on their unique features, rave reviews, and the unforgettable experiences they offer. Whether you’re traveling for adventure, here on a business trip, or just craving a luxurious escape, this list has something for everyone. Stick around, because number one is truly a must-see! And don’t forget—all the links to these incredible hotels are in the description below. Book your dream stay through those links to support the channel while snagging the perfect spot!"""

        best_outro_content = f"""Okay, guys, that’s it for today’s list of the Best Hotels in {place}! If you're ready to book your stay, all the links to these amazing hotels are right there in the description below—super easy to access. Thanks for watching, and if you found this helpful, don’t forget to hit that like button, subscribe, and ring the bell for more travel guides. Catch you in the next one!"""

        try:
            # Write content to files
            with open(os.path.join(best_intro_dir, "best_intro.txt"), "w") as intro_file:
                intro_file.write(best_intro_content)
            print(f"Intro content successfully written to '{best_intro_dir}/best_intro.txt'.")

            with open(os.path.join(best_outro_dir, "best_outro.txt"), "w") as outro_file:
                outro_file.write(best_outro_content)
            print(f"Outro content successfully written to '{best_outro_dir}/best_outro.txt'.")
        except Exception as e:
            print(f"Error writing to files: {e}")
            return

        # After generating the intro and outro files, you can run the next script (e.g., htl4.py)
        try:
            # Assuming you want to run htl4.py after successful execution
            print("Running htl4.py...")
            subprocess.run(["python", "htl4.py"], check=True)
            print("htl4.py executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running htl4.py: {e}")

    else:
        print("No places found in the 'places' directory. Please add at least one place file.")

if __name__ == "__main__":
    main()
