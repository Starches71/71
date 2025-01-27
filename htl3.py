
import os
import subprocess

places_dir = "places"  # Path to the places directory
best_intro_dir = "best_intro"  # Path to the best_intro directory               best_outro_dir = "best_outro"  # Path to the best_outro directory               
# List all files in the places directory
places = os.listdir(places_dir)         
# Check if there are any files in the places directory                          if places:
    # Get the first file in the list of places
    first_file = places[0]

    # Open the first file and read its contents
    with open(os.path.join(places_dir, first_file), "r") as file:
        place = file.readline().strip()  # Read the first line and remove any extra spaces or newlines

    # Define the content for best_intro and best_outro, replacing {place}
    best_intro_content = f"""Looking for the best places to stay in {place}? I’ve carefully handpicked the top hotels based on their unique features, rave reviews, and the unforgettable experiences they offer. Whether you’re traveling for adventure, here on a business trip, or just craving a luxurious escape, this list has something for everyone. Stick around, because number one is truly a must-see! And don’t forget—all the links to these incredible hotels are in the description below. Book your dream stay through those links to support the channel while snagging the perfect spot!"""

    best_outro_content = f"""Okay, guys, that’s it for today’s list of the Best Hotels in {place}! If you're ready to book your stay, all the links to these amazing hotels are right there in the description below—super easy to access. Thanks for watching, and if you found this helpful, don’t forget to hit that like button, subscribe, and ring the bell for more travel guides. Catch you in the next one!"""

    # Write content to files
    with open(os.path.join(best_intro_dir, "best_intro.txt"), "w") as intro_file:
        intro_file.write(best_intro_content)

    with open(os.path.join(best_outro_dir, "best_outro.txt"), "w") as outro_file:
        outro_file.write(best_outro_content)

    print(f"Files have been created successfully in '{best_intro_dir}' and '{best_outro_dir}' directories.")

    # Activate htl4.py script after generating the intro and outro files
    subprocess.run(["python", "htl4.py"])  # Run the htl4.py script

else:
    print("No places found in the 'places' directory. Please add at least one place file.")
