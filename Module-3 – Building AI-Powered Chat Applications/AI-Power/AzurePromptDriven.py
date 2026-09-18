from openai import OpenAI
from dotenv import load_dotenv
import os

client = OpenAI(
    api_key="",
    base_url=""
)

prompt = input("Enter your prompt: ")

response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print("\nAI:", response.choices[0].message.content)