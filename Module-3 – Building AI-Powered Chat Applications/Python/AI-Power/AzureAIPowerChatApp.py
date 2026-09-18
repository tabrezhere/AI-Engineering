
from openai import OpenAI
from dotenv import load_dotenv
import os


# --------------------------------
# Azure OpenAI / OpenAI Configuration
# --------------------------------

API_KEY = ""
BASE_URL = ""

client = OpenAI(
    api_key="",
    base_url=""
)

print("===================================")
print("       Python AI Chat Assistant")
print("===================================")
print("Type 'exit' to close the application")
print()


# --------------------------------
# Conversation History
# --------------------------------

messages = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant. Answer in simple English."
    }
]


# --------------------------------
# Chat Loop
# --------------------------------

while True:

    user_input = input("You: ")

    # Exit application
    if user_input.lower() == "exit":
        print("AI: Goodbye! 👋")
        break

    # Add user message
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Send conversation to AI
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages
    )

    # Get AI response
    ai_response = response.choices[0].message.content

    # Add AI response to conversation
    messages.append(
        {
            "role": "assistant",
            "content": ai_response
        }
    )

    print("AI:", ai_response)
    print()
