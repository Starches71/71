
import os
from groq import Groq
import time

# Initialize Groq client with your API key
client = Groq(api_key="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")

# Define the prompt to be used
prompt = """Give me random gadget that will make me wonder, or unusual, or strange. Give me the gadget that will make people wonder its presence. The gadget must be on Amazon store, also it must be halal in Islam, not abusive, not offensive, etc. Mention just the name of the product, no description, just the name."""

# Function to query Groq with the provided prompt
def query_groq():
    conversation_history = [{"role": "user", "content": prompt}]
    try:
        completion = client.chat.completions.create(
            model="Llama-3.3-70b-Versatile",
            messages=conversation_history,
            temperature=0,
            max_tokens=1024,
            top_p=0,
            stream=False,
        )
        # Extract and print the response content
        response_content = completion.choices[0].message.content if completion.choices else "No content found"
        print(f"Response: {response_content}")
        return response_content
    except Exception as e:
        print(f"Error while querying Groq: {e}")
        return None

# Function to run the query 20 times and print results
def run_multiple_queries():
    print("Running the query 20 times...")
    results = []
    for i in range(20):
        print(f"Run {i + 1}...")
        result = query_groq()
        if result:
            results.append(result)
        time.sleep(5)  # Add a small delay between requests to avoid hitting rate limits
    return results

if __name__ == "__main__":
    results = run_multiple_queries()
    print("\nFinal Results:")
    for idx, result in enumerate(results, start=1):
        print(f"Run {idx}: {result}")
