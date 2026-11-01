import os
from openai import OpenAI
from dotenv import load_dotenv
import json
import requests
from pydantic import BaseModel,Field
from typing import Optional

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

def get_weather_info(city: str):
    url=f"https://wttr.in/{city.lower()}?format=%C+%t"
    response=requests.get(url)

    if response.status_code==200:
        return f"The weather in {city} is: {response.text}"

    return "Sorry, I couldn't retrieve the weather information at this time."


available_tools = {
    "get_weather_info": get_weather_info
}

SYSTEM_PROMPT="""
    You are an expert AI assistant i nresolving user queries using chain of thought,You work on START,PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done.The PLAN can be multiple steps.
    Once you think enough PLAN has been done , finally you can give an OUTPUT.
    You can also call a tool if you think it is necessary to get the answer for the user query. from the list of available tools below.
    For every tool call wait for the observe step which is teh output of from the called tool and then continue with the PLAN and finally OUTPUT.

    Rules:
    -Strictly follow the given JSON format for output.
    -Only run one step at a time.
    -The sequence of steps is START(where user gives an input),PLAN(That can be multiple times) and finally OUTPUT(which is going to be displayed to the user).

    Output JSON Format:
    {"step":"START" | "PLAN" | "OUTPUT" | "TOOL","content":"string","tool":"string","input":"string","output":"string"} }

    Available Tools:
    1. get_weather_info(city: str) -> str: This tool retrieves the current weather information for a specified city. It returns a string containing the weather description and temperature.

    Example 1:
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

    Example 2:
        START: {"step":"START","content":"Hey , can you tell me the current weather in New York?"}
        PLAN: {"step":"PLAN","content":"Seems like user is interested in knowing the weather information about New York" }
        PLAN: {"step":"PLAN","content":"Lets see if we have any available tools from the list of available tools" }
        PLAN: {"step":"PLAN","content":"Great! We have the get_weather_info tool available." }
        PLAN: {"step":"PLAN","content":"I need to call the get_weather_info tool with the city name." }
        PLAN: {"step":"TOOL","tool":"get_weather_info","input":"New York"} }
        PLAN: {"step":"OBSERVE","tool":"get_weather_info","output":"The weather in New York is: Partly cloudy, 22°C" }
        PLAN: {"step":"PLAN","content":"Great! The weather information for New York has been retrieved." }
        
        OUTPUT: {"step":"OUTPUT","content":"The current weather in New York is: Partly cloudy, 22°C"}

"""

print("\n\n\n")

#This is a Pydantic model to validate the output from the LLM.helps in ensuring that the output adheres to the expected structure and types, making it easier to handle and process the data.
class MyOutputModel(BaseModel):
    step: str=Field(..., description="The current step in the reasoning process: START, PLAN, TOOL, OBSERVE, or OUTPUT")
    content: Optional[str]=Field(None, description="The content or message associated with the current step")
    tool: Optional[str]=Field(None, description="The name of the tool to be called, if applicable")
    input: Optional[str]=Field(None, description="The input for the tool, if applicable") 

message_history=[
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    },
]

while True:
    user_query=input("Enter your query: ")
    message_history.append({
        "role": "user",
        "content": user_query
    })

    while True:
        response = client.chat.completions.parse(
        model="gpt-4o",  # Ensure exact model ID
        response_format=MyOutputModel,
        messages=message_history,
    )
        raw_result=response.choices[0].message.content
        message_history.append({
            "role": "assistant",
            "content": raw_result
        })
        parsed_result=response.choices[0].message.parsed

        step = parsed_result.step
        content = parsed_result.content

        if step == "START":
            print("Starting LLM reasoning...", content)
            message_history.append({"role": "user", "content": "Continue."})
            continue

        if step == "PLAN":
            print("Planning and thinking process...", content)
            message_history.append({"role": "user", "content": "Continue."})
            continue

        if step=="TOOL":
            tool_to_call=parsed_result.tool
            tool_input=parsed_result.input
            print(f"Calling tool: {tool_to_call} with input: {tool_input}")

            tool_response=available_tools[tool_to_call](tool_input)
            print(f"Tool response: {tool_response}")
            message_history.append({
                "role": "developer",
                "content": json.dumps({
                    "step":"OBSERVE",
                    "tool":tool_to_call,
                    "input":tool_input,
                    "output":tool_response
                })
            })
            continue

        if step == "OUTPUT":
            print("\nFinal Output:\n", content)
            break


print("\n\n\n")


