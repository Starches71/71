
import os
from groq import Groq
import subprocess

# Initialize Groq client with your API key
client = Groq(api_key="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")

# File paths
city_file = "city.txt"
country_file = "country.txt"
places_dir = "places"

# Ensure the 'places' directory exists
os.makedirs(places_dir, exist_ok=True)


def query_admin_divisions(country_name):
    """
    Query Groq for the list of first/high-level administrative divisions in the specified country.
    Saves the result in city.txt.
    """
    query = f"List all first-level administrative divisions in {country_name}. Provide only their names, one per line, without any additional details or comments."
    conversation_history = [{"role": "user", "content": query}]

    try:
        # Make a request to Groq
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversation_history,
            temperature=0,
            max_tokens=1024,
            top_p=0,
            stream=False,
        )

        # Extract the response content directly from the completion
        response_content = (
            completion.choices[0].message.content if completion.choices else "No content found"
        )
        print(f"Groq Response for {country_name}:\n{response_content}")

        # Save the result in city.txt
        with open(city_file, "w") as file:
            file.write(response_content.strip())
        print(f"Administrative divisions saved in {city_file}\n")

        # Commit and push the updated city.txt to the repository
        subprocess.run(["git", "add", city_file])
        subprocess.run(["git", "commit", "-m", f"Update city.txt for {country_name}"])
        subprocess.run(["git", "push"])
        print(f"Updated {city_file} pushed to the repository.\n")

    except Exception as e:
        print(f"Error while querying Groq for {country_name}: {e}\n")


def process_country():
    """
    Process the first country from country.txt, fetch its first-level administrative divisions, and save them in city.txt.
    """
    try:
        # Read the first country name
        with open(country_file, "r") as file:
            countries = [line.strip() for line in file.readlines() if line.strip()]

        if countries:
            first_country = countries[0]
            print(f"Processing first country: {first_country}")

            # Query administrative divisions for the first country
            query_admin_divisions(first_country)

            # Remove the first country from the list
            countries.pop(0)

            # Write the updated list back to country.txt
            with open(country_file, "w") as file:
                file.write("\n".join(countries))
            print(f"Removed {first_country} from {country_file}\n")

            # Commit and push the updated country.txt to the repository
            subprocess.run(["git", "add", country_file])
            subprocess.run(["git", "commit", "-m", f"Update country.txt after processing {first_country}"])
            subprocess.run(["git", "push"])
            print(f"Updated {country_file} pushed to the repository.\n")
        else:
            print("No countries found in country.txt.")

    except FileNotFoundError:
        print(f"Error: {country_file} not found.\n")


def process_city():
    """
    Process the first administrative division from city.txt and send it to the 'places' directory.
    """
    try:
        # Read the first administrative division name
        with open(city_file, "r") as file:
            divisions = [line.strip() for line in file.readlines() if line.strip()]

        if divisions:
            first_division = divisions[0]
            print(f"Processing first administrative division: {first_division}")

            # Save the administrative division in the places directory
            with open(os.path.join(places_dir, f"{first_division}.txt"), "w") as file:
                file.write(first_division)
            print(f"Saved {first_division} in {places_dir}\n")

            # Remove the first administrative division from the file
            divisions.pop(0)

            # Write the updated list back to city.txt
            with open(city_file, "w") as file:
                file.write("\n".join(divisions))
            print(f"Removed {first_division} from {city_file}\n")
        else:
            print("No administrative divisions found in city.txt.")
            process_country()  # Process the first country if city.txt is empty

    except FileNotFoundError:
        print(f"Error: {city_file} not found.")
        process_country()  # Process the first country if city.txt is missing


def trigger_htl1():
    """
    Run htl1.py after processing the administrative division.
    """
    try:
        os.system("python3 htl1.py")
        print("htl1.py has been triggered.\n")
    except Exception as e:
        print(f"Error while triggering htl1.py: {e}\n")


if __name__ == "__main__":
    # Check if city.txt has content
    if os.path.exists(city_file) and os.stat(city_file).st_size > 0:
        process_city()  # Process the first administrative division
        trigger_htl1()  # Activate htl1.py
    else:
        # If city.txt is empty, process the first country
        process_country()
