import os
from groq import Groq

# Initialize Groq client with your API key
client = Groq(api_key="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")

# File paths
city_file = "city.txt"
country_file = "country.txt"
places_dir = "places"

# Ensure the 'places' directory exists
os.makedirs(places_dir, exist_ok=True)

def query_cities(country_name):
    """
    Query Groq for the list of cities in the specified country.
    Saves the result in city.txt.
    """
    query = f"Mention me all cities in {country_name}, without any additional details."
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
        response_content = completion.choices[0].message.content if completion.choices else "No content found"
        print(f"Groq Response for {country_name}:\n{response_content}")

        # Save the result in city.txt
        with open(city_file, "w") as file:
            file.write(response_content.strip())
        print(f"Cities saved in {city_file}\n")
    
    except Exception as e:
        print(f"Error while querying Groq for {country_name}: {e}\n")

def process_country():
    """
    Process the first country from country.txt, fetch its cities, and save them in city.txt.
    """
    try:
        # Read the first country name
        with open(country_file, "r") as file:
            countries = [line.strip() for line in file.readlines() if line.strip()]
        
        if countries:
            first_country = countries[0]
            print(f"Processing first country: {first_country}")

            # Query cities for the first country
            query_cities(first_country)
            
            # Remove the first country from the file
            with open(country_file, "w") as file:
                file.write("\n".join(countries[1:]))
            print(f"Removed {first_country} from {country_file}\n")
        else:
            print("No countries found in country.txt.")
    
    except FileNotFoundError:
        print(f"Error: {country_file} not found.\n")

def process_city():
    """
    Process the first city from city.txt and send it to the 'places' directory.
    """
    try:
        # Read the first city name
        with open(city_file, "r") as file:
            cities = [line.strip() for line in file.readlines() if line.strip()]
        
        if cities:
            first_city = cities[0]
            print(f"Processing first city: {first_city}")

            # Save the city in the places directory
            with open(os.path.join(places_dir, f"{first_city}.txt"), "w") as file:
                file.write(first_city)
            print(f"Saved {first_city} in {places_dir}\n")
            
            # Remove the first city from the file
            with open(city_file, "w") as file:
                file.write("\n".join(cities[1:]))
            print(f"Removed {first_city} from {city_file}\n")
        else:
            print("No cities found in city.txt.")
    
    except FileNotFoundError:
        print(f"Error: {city_file} not found.\n")

def trigger_htl1():
    """
    Run htl1.py after processing the city.
    """
    try:
        os.system("python3 htl1.py")
        print("htl1.py has been triggered.\n")
    except Exception as e:
        print(f"Error while triggering htl1.py: {e}\n")

if __name__ == "__main__":
    # Check if city.txt has content
    if os.path.exists(city_file) and os.stat(city_file).st_size > 0:
        process_city()  # Process the first city
        trigger_htl1()  # Activate htl1.py
    else:
        # If city.txt is empty, process the first country
        process_country()
