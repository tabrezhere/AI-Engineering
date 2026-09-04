
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# ---------------------------------------
# 1. Load .env from the application folder
# ---------------------------------------

env_file = Path(__file__).parent / ".env"

print("Loading environment file:")
print(env_file)

load_dotenv(dotenv_path=env_file, override=True)


# ---------------------------------------
# 2. Read configuration
# ---------------------------------------

API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")


# ---------------------------------------
# 3. Display configuration
# ---------------------------------------

print("\nChecking configuration...")

print("API Key:",
      "Loaded" if API_KEY else "Missing")

print("Endpoint:")
print(ENDPOINT)

print("Deployment:")
print(DEPLOYMENT)


# ---------------------------------------
# 4. Validate configuration
# ---------------------------------------

if not API_KEY:
    raise Exception("API key is missing")

if not ENDPOINT:
    raise Exception("Endpoint is missing")

if not DEPLOYMENT:
    raise Exception("Deployment name is missing")


# ---------------------------------------
# 5. Create Azure OpenAI client
# ---------------------------------------

client = OpenAI(
    api_key=API_KEY,
    base_url=ENDPOINT
)


# ---------------------------------------
# 6. Send actual request
# ---------------------------------------

try:

    response = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[
            {
                "role": "user",
                "content": "Explain Artificial Intelligence in simple English."
            }
        ]
    )

    print("\nCONNECTED ✅")

    print("\nAI RESPONSE:")
    print(response.choices[0].message.content)


except Exception as e:

    print("\nCONNECTION FAILED ❌")

    print("Error type:")
    print(type(e).__name__)

    print("\nError message:")
    print(e)
