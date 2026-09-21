import os
from openai import OpenAI
from dotenv import load_dotenv
import json

# Load .env file explicitly
load_dotenv()

# Verify variable name
api_key = os.getenv("OPENAI_API_KEY")

# Print first 5 chars to verify key loading without exposing it
if not api_key:
    print(" ERROR: OPENAI_API_KEY is missing or None!")
else:
    print(f" Key Loaded Successfully: {api_key[:5]}...")

client = OpenAI(
    api_key=api_key,
    
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

print("\n\n\n")

message_history=[
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    },
]

user_query=input("Enter your query: ")
message_history.append({
    "role": "user",
    "content": user_query
})

while True:
    response = client.chat.completions.create(
    model="gpt-4o",  # Ensure exact model ID
    response_format={"type": "json_object"},
    messages=message_history,
)
    raw_result=response.choices[0].message.content
    message_history.append({
        "role": "assistant",
        "content": raw_result
    })
    parsed_result=json.loads(raw_result)

    step = parsed_result.get("step")
    content = parsed_result.get("content")

    if step == "START":
        print("Starting LLM reasoning...", content)
        message_history.append({"role": "user", "content": "Continue."})
        continue

    if step == "PLAN":
        print("Planning and thinking process...", content)
        message_history.append({"role": "user", "content": "Continue."})
        continue

    if step == "OUTPUT":
        print("\nFinal Output:\n", content)
        break


print("\n\n\n")


