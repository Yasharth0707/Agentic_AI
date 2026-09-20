import os
from openai import OpenAI
from dotenv import load_dotenv
import json

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

SYSTEM_PROMPT="""
    You are an expert AI assistant i nresolving user queries using chain of thought,You work on START,PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done.The PLAN can be multiple steps.
    Once you think enough PLAN has been done , finally you can give an OUTPUT.

    Rules:
    -Strictly follow the given JSON format for output.
    -Only run one step at a time.
    -The sequence of steps is START(where user gives an input),PLAN(That can be multiple times) and finally OUTPUT(which is going to be displayed to the user).

    Output JSON Format:
    {"step":"START" | "PLAN" | "OUTPUT","content":"string"}

    Example:
    START: {"step":"START","content":"Hey , can u solve 2+3*5/10 for me?"}
    PLAN: {"step":"PLAN","content":"Seems like user is interested in solving a math problem." }
    PLAN: {"step":"PLAN","content":"Looking at the problem we should solve it using BODMAS" }
    PLAN: {"step":"PLAN","content":"Yes,the BODMAS is the correct thing to be done here" }
    PLAN: {"step":"PLAN","content":"First we multiply 3 and 5 which would give us 15" }
    PLAN: {"step":"PLAN","content":"Now the expression becomes 2+15/10" }
    PLAN: {"step":"PLAN","content":" we divide 15 by 10 which would give us 1.5" }
    PLAN: {"step":"PLAN","content":"Now the expression becomes 2+1.5" }
    PLAN: {"step":"PLAN","content":"Finally we add 2 and 1.5 which would give us 3.5" }
    OUTPUT: {"step":"OUTPUT","content":"The final answer is 3.5"}

"""

response = client.chat.completions.create(
    model="gemini-3.6-flash",
    response_format={"type": "json_object"},
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "Hey , write a code to add n numbers in c++"
            
        },
        #Manually keep adding messages to History to keep the context of the conversation
        {
            "role": "assistant",
            "content":json.dumps({"step":"PLAN","content":"User is interested in adding n numbers in c++"})
        },
        {
        "role": "user",
        "content": "Continue with the next PLAN or OUTPUT step."  # Added user turn
        },
        {
            "role": "assistant",
            "content":json.dumps({"step":"PLAN","content":"I will construct a standard C++ program that reads the integer 'n', then iterates 'n' times using a loop to collect inputs and compute their total sum, finally printing the result."})
        },
        {
            "role": "user",
            "content": "Continue with the next PLAN or OUTPUT step."  # Added user turn
        }
        
    ]
)

print(response.choices[0].message.content)