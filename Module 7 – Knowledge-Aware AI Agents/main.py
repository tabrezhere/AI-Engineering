from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

# --------------------------------
# Load environment variables
# --------------------------------


# --------------------------------
# OpenAI Client
# --------------------------------

client = OpenAI(
    api_key="",
    base_url=""
)

# --------------------------------
# FastAPI Application
# --------------------------------

app = FastAPI(
    title="AI Teaching Agent",
    description="AI Teaching Agent REST API",
    version="1.0"
)

# --------------------------------
# Read Knowledge content
# --------------------------------

try:
    with open("Knowledge.txt", "r", encoding="utf-8") as file:
        readme_content = file.read()

except FileNotFoundError:
    readme_content = ""


# --------------------------------
# Request Model
# --------------------------------

class ChatRequest(BaseModel):
    question: str


# --------------------------------
# Response Model
# --------------------------------

class ChatResponse(BaseModel):
    question: str
    answer: str


# --------------------------------
# System Prompt
# --------------------------------

system_prompt = f"""
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

--------------------------------
KNOWLEDGE FROM Knowledge.txt
--------------------------------

The following content comes from Knowledge.txt.

Use this information when answering questions.
If the answer is not available in the Knowledge,
use your general knowledge.

Knowledge CONTENT:

{readme_content}

--------------------------------
END Knowledge
--------------------------------
"""


# --------------------------------
# Chat API
# --------------------------------

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    try:

        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": request.question
            }
        ]

        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=messages
        )

        ai_response = response.choices[0].message.content

        return ChatResponse(
            question=request.question,
            answer=ai_response
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )


# --------------------------------
# Health Check
# --------------------------------

@app.get("/")
def root():

    return {
        "message": "AI Teaching Agent is running",
        "status": "success"
    }