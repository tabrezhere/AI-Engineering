
import os
import json

from openai import OpenAI
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
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
    description="Billing, Loan and Network Agents"
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

def identify_intent(question: str) -> str:
    """Identify which specialist should answer."""

    prompt = """
    You are an Intent Identifier.

    Classify the question into exactly one category:

    billing - bills, invoices, charges, payments, refunds
    loan    - loans, EMI, interest rates, repayment
    network - internet, Wi-Fi, router, connectivity, speed
    other   - anything unrelated to these categories

    Return only valid JSON.

    Example:
    {"intent": "billing"}
    """

    result = ask_ai(prompt, question)

    try:
        data = json.loads(result)
        intent = str(data.get("intent", "")).lower().strip()

        if intent in {"billing", "loan", "network", "other"}:
            return intent

    except (json.JSONDecodeError, AttributeError):
        pass

    # Do not accidentally route an unclassified question.
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


# =========================================
# 7. Agent Registry / Router
# =========================================

AGENTS = {
    "billing": billing_agent,
    "loan": loan_agent,
    "network": network_agent
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
            "Network Agent"
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
                    "I can help with billing, loans, "
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
