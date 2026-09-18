from openai import OpenAI
from dotenv import load_dotenv
import os


# --------------------------------
# Azure OpenAI / OpenAI Configuration
# --------------------------------



client = OpenAI(
    api_key="",
    base_url=""
)

context = """
Student Name: Rahul
Course: AI Engineering
Attendance: 85%
"""

question = input("Student: ")

prompt = f"""
Use the following student information to answer the question.

Student Information:
{context}

Question:
{question}
"""

response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print("AI:", response.choices[0].message.content)