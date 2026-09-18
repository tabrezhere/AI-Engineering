from fastapi import FastAPI
from openai import OpenAI
import os

app = FastAPI()

# Azure AI / OpenAI client
client = OpenAI(
    api_key="",
    base_url=""
)

@app.get("/ask")
def ask(question: str):

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    answer = response.choices[0].message.content

    return {
        "question": question,
        "answer": answer
    }