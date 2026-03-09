from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPEN_ROUTER_API_KEY"),
)


res = client.chat.completions.create(
    model="openai/gpt-oss-120b:free",
    messages=[
        {"role": "developer", "content": "Talk like a pirate."},
        {
            "role": "user",
            "content": "How do I check if a Python object is an instance of a class?",
        },
    ],
    stream= False,
    temperature= 0.7
)

print(res)