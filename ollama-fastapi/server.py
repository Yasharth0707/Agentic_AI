from fastapi import FastAPI,Body
from ollama import Client

app = FastAPI()
client=Client(
    host="http://localhost:11434"
)


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/contact-us")
async def read_root():
    return {"email": "yasharthsoubhari@gmail.com"}

@app.post("/chat")
async def chat(
    message: str = Body(..., description="The message to send to the Ollama API")
):
    response=client.chat(model="llama3.1:8b", messages=[{"role": "user", "content": message}])

    return {"response": response.message.content}

# The messages line packages your prompt into the standard format that modern LLM APIs expect—telling the model, "Here is a message from the user."

# The return line unpacks the object that Ollama sends back, grabs just the text content of the model's reply, and sends it back to whoever called your API.