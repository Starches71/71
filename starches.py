import os
from groq import Groq

# Initialize Groq client with your API key
client = Groq(api_key="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")

# Directories for saving results
best = "best"
cheap = "cheap"
places_dir = "places"
files_dir = "files"
city_file = "city.txt"  # Path to city.txt (directly in the root of the repository)
places_file = os.path.join(places_dir, "places.txt")

# Ensure all directories exist
os.makedirs(best, exist_ok=True)
os.makedirs(cheap, exist_ok=True)
os.makedirs(places_dir, exist_ok=True)
os.makedirs(files_dir, exist_ok=True)

def initialize_files():
    """
    Ensure necessary files exist and handle missing files gracefully.
    """
    if not os.path.exists(city_file):
        print(f"Warning: {city_file} not found in the repository. Creating a placeholder file.")
        with open(city_file, "w") as city:
            city.write("ExampleCity\n")  # Add a default city if needed

    if not os.path.exists(places_file):
        print(f"{places_file} not found. Creating and adding the first place from {city_file}.")
        try:
            with open(city_file, "r") as city:
                cities = [line.strip() for line in city.readlines() if line.strip()]

            if cities:
                first_place = cities[0]

                # Save the first place to places.txt
                with open(places_file, "w") as places:
                    places.write(first_place + "\n")

                print(f"Saved {first_place} to {places_file}.")

                # Remove the first place from city.txt
                with open(city_file, "w") as city:
                    city.write("\n".join(cities[1:]))

                print(f"Removed {first_place} from {city_file}.")
            else:
                print(f"{city_file} is empty. Cannot populate {places_file}.")

        except Exception as e:
            print(f"Error while initializing files: {e}\n")

def query_hotels(place_name, query_type="best"):
    """
    Query Groq for the list of halal hotels based on the type ('best' or 'cheap') and place.
    Saves the result in the corresponding directory.
    """
    if query_type == "best":
        query = f"Mention me 7 best halal hotels (not resorts, inns etc) in {place_name}, mention me the hotels with high quality videos on youtube and with more online presence. Just mention, don't explain (i.e., mention hotels names only without any additional details; if it's not a hotel, don't include it in the list)."
        output_dir = best
    elif query_type == "cheap":
        query = f"Mention me 7 best cheap halal hotels (not resorts, inns etc) in {place_name}, mention me the hotels with high quality videos on youtube and with more online presence. Just mention, don't explain (mention hotels names only without any additional details; if it's not a hotel, don't include it in the list)."
        output_dir = cheap

    # Initialize the conversation history
    conversation_history = [{"role": "user", "content": query}]

    try:
        # Make a request to Groq
        completion = client.chat.completions.create(
            model="Llama3-8b-8192",
            messages=conversation_history,
            temperature=0,
            max_tokens=1024,
            top_p=0,
            stream=False,
        )

        # Extract the response content directly from the completion
        response_content = completion.choices[0].message.content if completion.choices else "No content found"

        print(f"Groq Response for {place_name} ({query_type}):\n{response_content}")

        # Save the result in a file
        file_name = os.path.join(output_dir, f"{place_name.replace(' ', '_')}_{query_type}_hotels.txt")
        with open(file_name, "w") as file:
            file.write(response_content)

        print(f"Results saved in {file_name}\n")

    except Exception as e:
        print(f"Error while querying Groq for {place_name} ({query_type}): {e}\n")

def process_places():
    """
    Read the place names from places.txt and query Groq for each place.
    """
    try:
        with open(places_file, "r") as file:
            places = [line.strip() for line in file.readlines() if line.strip()]

        for place in places:
            print(f"Processing place: {place}")

            # Query Groq for 'best' and 'cheap' halal hotels
            query_hotels(place, query_type="best")
            query_hotels(place, query_type="cheap")

            # Remove the city from city.txt after processing it
            with open(city_file, "r") as city:
                cities = [line.strip() for line in city.readlines() if line.strip()]

            if place in cities:
                cities.remove(place)

            with open(city_file, "w") as city:
                city.write("\n".join(cities))

            print(f"Removed {place} from {city_file}.")

        print("Hotel queries completed for all places.")

    except FileNotFoundError:
        print(f"Error: {places_file} not found.\n")

def trigger_htl2():
    """
    Run htl2.py after all hotel queries are done.
    """
    try:
        # Run htl2.py script
        os.system("python3 htl2.py")
        print("htl2.py has been triggered.")
    except Exception as e:
        print(f"Error while triggering htl2.py: {e}")

if __name__ == "__main__":
    initialize_files()  # Ensure necessary files exist
    process_places()  # Process places for hotel queries
    trigger_htl2()  # Activate htl2.py after the main process is completed
