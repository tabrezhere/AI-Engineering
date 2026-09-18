from openai import OpenAI
from dotenv import load_dotenv
import os

client = OpenAI(
    api_key="",
    base_url=""
)

def ask_ai(prompt):

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

answer = ask_ai("What is Artificial Intelligence?")
print(answer)

answer = ask_ai("Summarize: Python is a programming language used for AI.")
print(answer)

answer = ask_ai("Write Python code to check whether a number is even.")
print(answer)

answer = ask_ai("Translate 'Good Morning' into Hindi.")
print(answer)

