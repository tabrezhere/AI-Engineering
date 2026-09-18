from openai import OpenAI
from dotenv import load_dotenv
import os

client = OpenAI(
    api_key="",
    base_url=""
)

messages = [
    {
        "role": "system",
        "content": """
        You are a College AI Assistant.
        Help students with courses, subjects,
        attendance, exams and college information.
        Answer in simple English.
        """
    }
]

print("College AI Assistant")
print("Type 'exit' to stop\n")

while True:

    question = input("Student: ")

    if question.lower() == "exit":
        break

    messages.append({
        "role": "user",
        "content": question
    })

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages
    )

    answer = response.choices[0].message.content

    messages.append({
        "role": "assistant",
        "content": answer
    })

    print("College AI:", answer)
    print()