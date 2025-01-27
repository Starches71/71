
import os
from groq import Groq

# Define the directories
best_dir = "best"  # Directory where the hotel text files are located
places_dir = "places"  # Directory where the places are located
descriptions_dir = "best_descriptions"  # Directory to save descriptions

# Make sure the output directory exists
os.makedirs(descriptions_dir, exist_ok=True)

# Initialize the Groq client with the API key
client = Groq(api_key="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")


def get_best_hotel_file():
    """Get the first hotel file in the 'best' directory."""
    hotel_files = [f for f in os.listdir(best_dir) if f.endswith(".txt")]
    if hotel_files:
        return os.path.join(best_dir, hotel_files[0])  # Return the first file
    return None


def get_first_place_from_places():
    """Get the first place from the 'places' directory."""
    places_file = os.path.join(places_dir, "places.txt")
    if os.path.exists(places_file):
        with open(places_file, "r") as f:
            first_place = f.readline().strip()  # Read the first line
        return first_place
    print("Places file not found!")
    return None


def generate_description_for_hotel(hotel_name, place_name):
    """Generate an essay summary using the Groq API with streaming."""
    prompt = f"Write me an essay summary about {hotel_name} hotel in {place_name},essay should be 250words , dont include hotel features that are not allowed  Islam,dont add any opening or closing just the essay."

    try:
        # Send the prompt to Groq API and get the response
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_tokens=6040,
            top_p=1,
            stream=True,  # Enable streaming
            stop=None,
        )

        # Stream the response and collect content
        response_content = ""
        print(f"Response for {hotel_name}: ", end="")

        # Process each chunk of the streamed response
        for chunk in completion:
            delta = chunk.choices[0].delta.content or ""
            response_content += delta
            print(delta, end="", flush=True)

        print("\n")  # Newline after the response

        # Return the full description
        return response_content

    except Exception as e:
        print(f"Error generating description for {hotel_name}: {e}")
        return ""


def process_hotel_file(hotel_file):
    """Process the hotel file from the 'best' directory."""
    with open(hotel_file, "r") as f:
        hotel_list = f.readlines()

    # Get the first place name
    place_name = get_first_place_from_places()
    if not place_name:
        print("Place name is not available. Exiting process.")
        return

    # Process each hotel
    for i, hotel in enumerate(hotel_list, start=1):
        hotel = hotel.strip()  # Clean any surrounding whitespace
        if not hotel:  # Skip empty lines
            continue

        # Try to split based on the number at the beginning (e.g., "1. Hotel Name")
        hotel_parts = hotel.split(".", 1)  # Split into number and hotel name
        if len(hotel_parts) < 2:  # If the split doesn't result in two parts, skip this line
            print(f"Skipping invalid line: {hotel}")
            continue

        hotel_name = hotel_parts[1].strip()  # Get the hotel name (after the number)
        print(f"Processing hotel: {hotel_name}")

        # Generate a description for the hotel using the Groq API
        description = generate_description_for_hotel(hotel_name, place_name)

        if description:
            # Save the description in the best_descriptions directory with the correct number
            description_file = os.path.join(descriptions_dir, f"{hotel_parts[0]}. {hotel_name}.txt")
            with open(description_file, "w") as f:
                f.write(description)
            print(f"Description saved as: {description_file}")
        else:
            print(f"Failed to generate description for {hotel_name}.")


def main():
    """Main function to process the hotel file."""
    hotel_file = get_best_hotel_file()  # Get the hotel file in 'best' directory

    if not hotel_file:
        print("No hotel file found in the 'best' directory.")
        return

    process_hotel_file(hotel_file)

    # Now, run htl3.py at the end
    try:
        # Import and run the main function of htl3.py
        import htl3  # Assuming htl3.py is in the same directory
        print("Running htl3.py...")
        htl3.main()  # Call the main function of htl3.py
    except ImportError:
        print("Error: htl3.py not found or unable to import.")


if __name__ == "__main__":
    main()
