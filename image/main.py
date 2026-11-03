from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client=OpenAI()

response=client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
        "role": "user" ,
        "content": [
            {"type": "text" , "text" : "Generate a caption for this image."},
            {"type":"image_url", "image_url": {"url":"https://images.pexels.com/photos/38273820/pexels-photo-38273820.jpeg"}}
        ]
        }
    ]
)

print("Response:",response.choices[0].message.content)