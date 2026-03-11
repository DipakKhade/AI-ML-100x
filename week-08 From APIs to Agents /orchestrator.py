from openai import OpenAI
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain.tools import tool
import json
import subprocess
import wikipedia
import requests


load_dotenv()


researcher_agent = ChatOpenAI(
    api_key= os.environ.get('OPEN_ROUTER_API_KEY'),
    base_url='https://openrouter.ai/api/v1'
)

@tool
def research_over_a_topic(topic: str) -> str:
    """
    This tool will do research from the internet and wikipedia and get the most accurate information.
    """
    results = []

    try:
        wiki_summary = wikipedia.summary(topic, sentences=5, auto_suggest=True)
        results.append(f"## Wikipedia Summary\n{wiki_summary}")

        page = wikipedia.page(topic, auto_suggest=True)
        results.append(f"\n**Wikipedia Source:** {page.url}")
    except wikipedia.exceptions.DisambiguationError as e:
        try:
            wiki_summary = wikipedia.summary(e.options[0], sentences=5)
            results.append(f"## Wikipedia Summary (disambiguated to: {e.options[0]})\n{wiki_summary}")
        except Exception:
            results.append(f"## Wikipedia\nDisambiguous topic. Suggestions: {', '.join(e.options[:5])}")
    except wikipedia.exceptions.PageError:
        results.append(f"## Wikipedia\nNo Wikipedia page found for '{topic}'.")
    except Exception as e:
        results.append(f"## Wikipedia\nError fetching Wikipedia data: {str(e)}")

    try:
        ddg_url = "https://api.duckduckgo.com/"
        params = {
            "q": topic,
            "format": "json",
            "no_redirect": "1",
            "no_html": "1",
            "skip_disambig": "1",
        }
        response = requests.get(ddg_url, params=params, timeout=10)
        data = response.json()

        web_results = []

        if data.get("AbstractText"):
            web_results.append(f"**Abstract:** {data['AbstractText']}")
            if data.get("AbstractURL"):
                web_results.append(f"**Source:** {data['AbstractURL']}")

        if data.get("Answer"):
            web_results.append(f"**Direct Answer:** {data['Answer']}")

        related = data.get("RelatedTopics", [])
        if related:
            web_results.append("\n**Related Topics:**")
            for item in related[:5]:  # limit to top 5
                if isinstance(item, dict) and item.get("Text"):
                    web_results.append(f"- {item['Text']}")

        if web_results:
            results.append("\n## Web Research (DuckDuckGo)\n" + "\n".join(web_results))
        else:
            results.append("\n## Web Research (DuckDuckGo)\nNo structured web results found.")

    except Exception as e:
        results.append(f"\n## Web Research\nError fetching web data: {str(e)}")

    if not results:
        return f"No information found for topic: '{topic}'"

    return "\n".join(results)


researcher_agent_with_tools = researcher_agent.bind_tools([research_over_a_topic])

def call_researcher_agent_with_tools(prompt: str):
    res = researcher_agent_with_tools.invoke(prompt)
    print('---------------res from call_researcher_agent_with_tools-------------', res)

coder_agent = ChatOpenAI(
    api_key= os.environ.get('OPEN_ROUTER_API_KEY'),
    base_url='https://openrouter.ai/api/v1'
)

@tool
def run_command(cmd: list[str]):
    """
        this tool will can run a command on a local machine of user
        you can pass list of command flags to this tool
        e.g ["ls", "-l"]
    """
    result = subprocess.run([cmd], capture_output=True, text=True)
    print(result.stdout)

coder_agent_with_tools = coder_agent.bind_tools([run_command])

def call_coder_agent_with_tools(prompt: str):
    res = coder_agent_with_tools.invoke(prompt)
    print('res from call_coder_agent_with_tools ----', res)

orchestrator_agent = OpenAI(
    base_url='https://openrouter.ai/api/v1',
    api_key= os.environ.get('OPEN_ROUTER_API_KEY')
)

system_prompt = '''
    Hey you are a orchestrator and you orchestrator between the different agents 
        for now you have 2 againt
        Agent list:
            1. Researcher Agent
            2. Coding Agent
        
    you have to respond back me with the follwing type of json on the basis of the task asked by the user, also add a enhanced prmopt 

    {
        agent_to_use: researcher_agent | coder_agent,
        prompt: 'this is a enhanced prompt so that agent will do its work properly'
    }
    
    do not give reponse in any other format, use above format strictly, also make sure that it can split out a valid json when i do json.loads

'''

res = orchestrator_agent.chat.completions.create(
    model='openrouter/free',
    messages= [
        {'role': 'developer', 'content': system_prompt},
        {'role': 'user', 'content': 'give me a details of world war 3'}
    ]
)
orchestrator_agent_res = json.loads(res.choices[0].message.content)


agents = {
    'researcher_agent': call_researcher_agent_with_tools,
    'coder_agent': call_coder_agent_with_tools 
}

if orchestrator_agent_res['agent_to_use'] in agents:
    print('----------------calling-------------', orchestrator_agent_res['agent_to_use'])
    agents[orchestrator_agent_res['agent_to_use']](orchestrator_agent_res['prompt'])
    
