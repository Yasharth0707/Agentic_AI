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

# Zero Shot Prompting:Here the instruction is given directly to the model in the system message. The model is expected to follow the instruction and provide an appropriate response based on the given context.Also no prior example is given to the model in this case. The model is expected to generate a response based on its understanding of the instruction and the context provided in the system message.
SYSTEM_PROMPT="Your name is CodeGPT and you are a coding expert and code reviewer.You should answer questions and queries only related to coding and code review. If the question is not related to coding or code review, politely decline to answer and suggest that the user ask a different question."

response = client.chat.completions.create(
    model="gemini-3.6-flash",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "pls give me the dijkstra algorithm in python"
        }
    ]
)

print(response.choices[0].message.content)