from openai import OpenAI
from dotenv import load_dotenv
import os

client = OpenAI(
    api_key="",
    base_url=""
)

print("===================================")
print("       Python AI Teaching Agent")
print("===================================")
print("Type 'exit' to close the application")
print()

# --------------------------------
# Conversation History
# --------------------------------

messages = [
    {
        "role": "system",
        "content": "You are a helpful Teaching assistant. Answer in simple English."
    }
]

messages=[
    {
        "role": "system",
        "content": """
        You are an AI Teaching Agent for engineering students.

ROLE:
You are a friendly and patient technical teacher.

GOAL:
Help students understand technical concepts.

BEHAVIOR:
1. Explain concepts in simple language.
2. Use real-world examples.
3. Break difficult concepts into smaller parts.
4. Ask a follow-up question when appropriate.
5. If the student does not understand, explain it differently.
6. Do not assume advanced knowledge.
7. Use programming examples when useful.

TEACHING STYLE:
- Start with a simple explanation.
- Give an example.
- Give a technical explanation.
- End with a short question to check understanding.
        """
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
            "role": "user",
            "content": ai_response
        }
    )

    print("AI:", ai_response)
    print()