
import os
import json

from openai import OpenAI
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# =========================================
# AI Configuration
# =========================================

client = OpenAI(
    api_key="",
    base_url=""
)
MODEL = "gpt-4.1"

app = FastAPI(
    title="Multi-Agent AI System",
    description="Billing, Loan and Network Agents,teaching Agent,Legal Agent"
)

# ==============================
# CORS
# ==============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
# =========================================
# 2. Common AI Function
# =========================================

def ask_ai(system_prompt: str, question: str) -> str:
    """Send a question to the configured AI model."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0.2,
        max_tokens=400
    )

    return (
        response.choices[0].message.content
        or "Sorry, I could not generate an answer."
    )


# =========================================
# 3. Intent Identifier
# =========================================


#Identify Agent Intent
def identify_intent(question: str) -> str:
    """Identify the correct specialist agent."""

    text = question.lower().strip()

    # Step 1: Identify clear teaching-related questions
    teaching_keywords = [
        "artificial intelligence",
        "generative ai",
        "machine learning",
        "deep learning",
        "python",
        "programming",
        "teach me",
        "explain",
        "tutorial",
        "engineering",
        "coding",
        "c#",
        ".net",
        "fastapi",
        "openai",
        "multi-agent",
        "llm",
        "neural network",
        "data science"
    ]

    if any(keyword in text for keyword in teaching_keywords):
        return "teaching"

    # Step 2: Use OpenAI for other questions
    prompt = """
    Classify the question into exactly one category:
    billing, loan, network, teaching, or other.

    billing: invoices, payments, charges, refunds.
    loan: loans, EMI, interest rates, repayment.
    network: Wi-Fi, internet, router, connectivity.
    teaching: education, learning, technical concepts,
    programming, AI, engineering, tutorials and explanations.
    legal: laws, regulations, contracts, compliance.
    other: questions unrelated to these categories.

    Return only JSON:
    {"intent": "teaching"}
    """

    raw = ask_ai(prompt, question)

    try:
        raw = raw.strip()

        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1]
            raw = raw.rsplit("```", 1)[0].strip()

        result = json.loads(raw)
        intent = result.get("intent", "").lower()
        print(f"Identified intent: {intent}")
        if intent in {
            "billing", "loan", "network", "teaching","legal", "other"
        }:
            return intent

    except (json.JSONDecodeError, AttributeError):
        pass

    return "other"
# =========================================
# 4. Billing Agent
# =========================================

def billing_agent(question: str) -> str:

    prompt = """
    You are the Billing Agent.

    Your responsibilities:
    - Explain bills and invoices.
    - Explain possible additional charges.
    - Answer payment and refund questions.
    - Suggest steps to investigate billing problems.

    Use simple English.
    Do not invent customer account information.
    You do not have access to actual billing records.
    """

    return ask_ai(prompt, question)


# =========================================
# 5. Loan Agent
# =========================================

def loan_agent(question: str) -> str:

    prompt = """
    You are the Loan Agent.

    Your responsibilities:
    - Explain loans and EMI.
    - Explain interest rates and repayment.
    - Help with loan calculations when sufficient
      information is provided.
    - Explain loan tenure and repayment options.

    Use simple English.
    State assumptions for calculations.
    Do not claim access to real loan accounts.
    """

    return ask_ai(prompt, question)


# =========================================
# 6. Network Agent
# =========================================

def network_agent(question: str) -> str:

    prompt = """
    You are the Network Agent.

    Your responsibilities:
    - Troubleshoot internet connectivity.
    - Help with Wi-Fi and router problems.
    - Explain slow internet speed.
    - Suggest practical troubleshooting steps.

    Use simple English.
    Do not claim to have tested the actual network.
    """

    return ask_ai(prompt, question)


def teaching_agent(question: str) -> str:
    return ask_ai(
        """
        You are an AI Teaching Agent for engineering students.

        Your goal is to help students understand technical concepts.

        Adapt your explanation to the student's apparent knowledge
        level based on the available conversation context.

        BEGINNER:
        - Use simple language and analogies.
        - Avoid unnecessary technical terminology.
        - Explain concepts step by step.

        INTERMEDIATE:
        - Explain technical concepts clearly.
        - Provide practical examples and relevant terminology.
        - Include code examples when useful.

        ADVANCED:
        - Explain architecture, design patterns and implementation.
        - Discuss trade-offs and best practices.
        - Provide detailed technical examples when appropriate.

        TEACHING GUIDELINES:
        - Be patient, supportive and encouraging.
        - Break complex topics into smaller steps.
        - Use examples relevant to engineering students.
        - For programming questions, provide correct code and explain it.
        - For AI questions, explain concepts and practical applications.
        - Ask a short follow-up question when it helps learning.
        - Never assume the student already understands a concept.
        - Do not claim to know the student's skill level with certainty.

        Answer the student's question directly.
        """,
        question
    )


def Legal_agent(question: str) -> str:
    return ask_ai(
        """
        You are a Legal Agent. Answer legal questions about laws, regulations, contracts, and compliance clearly and accurately. Never invent legal information. Consider jurisdiction, mention uncertainties, protect privacy, and recommend consulting a qualified lawyer for complex matters. Decline unrelated queries.
        """,
        question
    )

# =========================================
# 7. Agent Registry / Router
# =========================================

AGENTS = {
    "billing": billing_agent,
    "loan": loan_agent,
    "network": network_agent,
    "teaching": teaching_agent,
    "legal": Legal_agent

}


# =========================================
# 8. API Request Model
# =========================================

class AskRequest(BaseModel):
    question: str = Field(
        min_length=3,
        max_length=2000
    )


# =========================================
# 9. Main Multi-Agent Endpoint
# =========================================

@app.get("/")
def home():

    return {
        "application": "Multi-Agent AI System",
        "agents": [
            "Billing Agent",
            "Loan Agent",
            "Network Agent",
            "Teaching Agent",
            "Legal Agent"
        ],
        "endpoint": "POST /ask"
    }


@app.post("/ask")
def ask(request: AskRequest):

    try:
        # Step 1: Identify the user's intent
        intent = identify_intent(request.question)

        # Step 2: Select the appropriate agent
        selected_agent = AGENTS.get(intent)

        # Step 3: Handle unsupported questions
        if selected_agent is None:

            return {
                "intent": intent,
                "agent": "General Assistant",
                "answer": (
                    "I can help with billing, loans, teaching"
                    "or network connectivity. "
                    "Please ask a related question."
                )
            }

        # Step 4: Execute the selected agent
        answer = selected_agent(request.question)

        # Step 5: Return the final response
        return {
            "intent": intent,
            "agent": intent.capitalize() + " Agent",
            "answer": answer
        }

    except Exception as exc:

        # Print detailed error in the server terminal.
        print(
            f"Multi-agent error: "
            f"{type(exc).__name__}: {exc}"
        )

        raise HTTPException(
            status_code=502,
            detail=(
                f"AI service error: "
                f"{type(exc).__name__}: {exc}"
            )
        ) from exc
