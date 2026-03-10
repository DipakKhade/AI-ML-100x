from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()

agent = OpenAI(
    base_url='https://openrouter.ai/api/v1',
    api_key= os.environ.get('OPEN_ROUTER_API_KEY')
)

system_prompt = '''
    Hey you are a orchestrator and you orchestrator between the different agents 
        for now you have 2 againt
        Agent list:
            1. Researcher Agent
            2. Coding Agent
        
    you have to respond back me with the follwing type of json on the basis of the task asked by the user

    {
        agent_to_use: researcher_agent | coding_agent
    }

'''

res = agent.chat.completions.create(
    model='openrouter/free',
    messages= [
        {'role': 'developer', 'content': system_prompt},
        {'role': 'user', 'content': 'write a rust fn to add vec of numbers'}
    ]
)

print(res.choices[0].message.content)