import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env file explicitly
load_dotenv()

# Verify variable name
api_key = os.getenv("GENAI_API_KEY")

# Print first 5 chars to verify key loading without exposing it
if not api_key:
    print(" ERROR: GENAI_API_KEY is missing or None!")
else:
    print(f" Key Loaded Successfully: {api_key[:5]}...")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-3.6-flash",
    messages=[
        {
            "role": "system",
            "content": "You are an expert in maths and answer questions and queries only related to mathematics. If the question is not related to mathematics, politely decline to answer and suggest that the user ask a different question."
        },
        {
            "role": "user",
            "content": "can u solve a+b whole squared?"
        }
    ]
)

print(response.choices[0].message.content)