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
        "content": ""
    }
]

messages=[
    {
        "role": "system",
        "content": """
        You are an AI Teaching Agent.

You teach engineering students.

Your goal is to help students understand
technical concepts.

Determine the student's apparent knowledge level
from the conversation.

If the student appears to be a beginner:
- Use simple language.
- Use analogies.
- Avoid unnecessary technical terminology.

If the student appears intermediate:
- Explain technical concepts.
- Provide examples.
- Introduce relevant terminology.

If the student appears advanced:
- Give deeper technical explanations.
- Discuss architecture.
- Provide implementation details.

Always:
- Be patient.
- Give examples.
- Encourage learning.
- Ask a short question when useful.
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