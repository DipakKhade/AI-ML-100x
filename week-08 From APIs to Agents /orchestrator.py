from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()

agent = OpenAI(
    base_url='https://openrouter.ai/api/v1',
    api_key= os.environ.get('OPEN_ROUTER_API_KEY')
)

res = agent.chat.completions.create(
    model='openrouter/free',
    messages= [
        {'role': 'user', 'content': 'hello sir'},
    ]
)

print(res)