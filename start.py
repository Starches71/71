import os
from groq import Groq

# Initialize Groq client with your API key
client = Groq(api_key="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")

# Directory for saving the results
places_dir = "places"
os.makedirs(places_dir, exist_ok=True)

def query_cities(country_name):
    """
    Query Groq for the list of cities in the specified country.
    Saves the result in the 'places' directory as a simple text file.
    """
    query = f"Mention me all cities in {country_name}, without any additional details."
    output_dir = places_dir

    # Initialize the conversation history
    conversation_history = [{"role": "user", "content": query}]

    try:
        # Make a request to Groq
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=conversation_history,
            temperature=0,
            max_tokens=1024,
            top_p=0,
            stream=False,
        )

        # Extract the response content directly from the completion
        response_content = completion.choices[0].message.content if completion.choices else "No content found"

        print(f"Groq Response for {country_name}:\n{response_content}")

        # Save the result as a simple text file containing city names
        file_name = os.path.join(output_dir, f"{country_name.replace(' ', '_')}_cities.txt")
        with open(file_name, "w") as file:
            file.write(response_content.strip())

        print(f"Results saved in {file_name}\n")

    except Exception as e:
        print(f"Error while querying Groq for {country_name}: {e}\n")

def process_first_country():
    """
    Read the first country name from country.txt and query Groq for its cities.
    """
    country_file = "country.txt"

    try:
        # Read country names from the file
        with open(country_file, "r") as file:
            countries = [line.strip() for line in file.readlines() if line.strip()]

        if countries:
            first_country = countries[0]
            print(f"Processing first country: {first_country}")

            # Query Groq for cities in the first country
            query_cities(first_country)

            print("City query completed for the first country.")
        else:
            print("No countries found in the file.")

    except FileNotFoundError:
        print(f"Error: {country_file} not found.\n")

def trigger_htl1():
    """
    Run htl1.py after the city query is done.
    """
    try:
        # Run htl1.py script
        os.system("python3 htl1.py")
        print("htl1.py has been triggered.")
    except Exception as e:
        print(f"Error while triggering htl1.py: {e}")

if __name__ == "__main__":
    process_first_country()
    trigger_htl1()  # Activate htl1.py after the main process is completed
