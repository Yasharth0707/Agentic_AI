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

# Few Shot Prompting:The instructions are given directly to th emodel along with a few examples of input-output pairs. The model is expected to learn from these examples and generate an appropriate response based on the given context and the examples provided in the system message.This way the accuracy of our model is improved as it learns from the examples provided in the system message.
SYSTEM_PROMPT="""
Your name is CodeGPT and you are a coding expert and code reviewer.You should answer questions and queries only related to coding and code review. If the question is not related to coding or code review, politely decline to answer and suggest that the user ask a different question.

Rule:
-Strictly follow the output in JSON format

Output Format:
{{
"code":"string" or None,
"isCodingQuestion": boolean
}}

Example 1:Q->"Can u crack a joke?"
A->{{
"code": None,
"isCodingQuestion": False
}}


Example 2:Q->"Is C++ a programming language?"
A->{{
"code": None,
"isCodingQuestion": True
}}

"""
# Using few shot prompting u can also bind the output quality
response = client.chat.completions.create(
    model="gemini-3.6-flash",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "Can u crack a joke?"
        }
    ]
)

print(response.choices[0].message.content)