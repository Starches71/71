
import requests
from groq import Groq
import sys

def process_product(api_key, product):
    client = Groq(api_key=api_key)

    prompt = f'Is the {product} a real product on Amazon or just a product category? Answer p if it is a product, and answer c if it is a category. Just answer p or c only.'
    conversation_history = [{'role': 'user', 'content': prompt}]

    completion = client.chat.completions.create(
        model='Llama-3.3-70b-Versatile',
        messages=conversation_history,
        temperature=0,
        max_tokens=10,
        top_p=0,
        stream=False
    )

    response_content = completion.choices[0].message.content.strip().lower() if completion.choices else 'invalid'
    return response_content

def main():
    api_key = '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'  # Your API key
    product = sys.argv[1]  # Get product from argument passed to the script
    response = process_product(api_key, product)
    print(response)

if __name__ == '__main__':
    main()
