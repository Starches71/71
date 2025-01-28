
import os
import subprocess

# Paths for directories
descriptions_dir = "best_descriptions"
cleaned_dir = "best_clean"

# Static intro and outro templates
intro_templates = [
    "Coming in at number 7, we have {Hotel Name}",
    "At number 6 we have {Hotel Name},",
    "Number 5 on the list is {Hotel Name},",
    "Number 4 is {Hotel Name},",
    "Taking the number 3 spot is {Hotel Name},",
    "Coming in at number 2 is {Hotel Name},",
    "And finally, number 1 today is {Hotel Name}"
]

outro_templates = [
    "If you’re ready to book your stay at {Hotel Name}, check out the link in the description below.",
    "Want to stay at {Hotel Name}? Click the link in the description to book your stay and enjoy all the fantastic amenities this hotel has to offer.",
    "Looking for a comfortable stay at {Hotel Name}? You can book it through the link in the description.",
    "Don't miss out on the amazing {Hotel Name}! Book now using the link in the description.",
    "Ready to experience {Hotel Name}? Book through the link in the description.",
    "For an unforgettable stay at {Hotel Name}, just click the link in the description to book your stay.",
    "You can book your stay at {Hotel Name} through the link in the description."
]

# Ensure the cleaned directory exists
os.makedirs(cleaned_dir, exist_ok=True)

# List all hotel description files in the directory
hotel_files = os.listdir(descriptions_dir)

# Sort the hotel files to ensure they are processed in numerical order
hotel_files.sort(key=lambda x: int(x.split(".")[0]))

# Process each file in the descriptions directory
for index, hotel_file in enumerate(hotel_files):
    # Extract the hotel number from the filename (e.g., "1. Four Seasons Hotel Riyadh.txt")
    hotel_number = int(hotel_file.split(".")[0])  # Extract the number (e.g., 1, 2, 3, etc.)
    hotel_name = hotel_file.split(".")[1].strip()  # Extract the hotel name from the filename

    # Read the hotel description from the file
    with open(os.path.join(descriptions_dir, hotel_file), "r") as file:
        hotel_description = file.read().strip()  # Get the description and remove extra spaces/newlines

    # Get the corresponding intro and outro for this hotel
    intro = intro_templates[6 - index].replace("{Hotel Name}", hotel_name)  # Reverse the order for correct matching
    outro = outro_templates[6 - index].replace("{Hotel Name}", hotel_name)  # Reverse the order for correct matching

    # Create the cleaned hotel description with intro, the hotel description, and outro
    cleaned_content = f"{intro}\n\n{hotel_description}\n\n{outro}"

    # Save the cleaned content in the 'best_clean' directory with '.clean' extension
    cleaned_file_path = os.path.join(cleaned_dir, f"{hotel_number}. {hotel_name}.clean")
    with open(cleaned_file_path, "w") as cleaned_file:
        cleaned_file.write(cleaned_content)

    print(f"Cleaned file saved: {cleaned_file_path}")

# Run htl5.py after processing all the files
subprocess.run(["python", "htl5.py"])  # Activate the htl5.py script
