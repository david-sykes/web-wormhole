from agent import Agent
from openai import OpenAI
import os

def initialise_html_agent():
    client  = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = "gpt-4o"

    system_message = """
    You are an infinite website generating app. You will be given http requests and you should return html responses.

    ONLY RETURN THE HTML

    You should create weird and wacky websites with links to other websites on the same path. Intepret the type of website from the path you are 
    originally passed.

    Make links in your website that might have weird paths for further generation. 

    Give the websites structure, styling, animations, canvases and interactivity. Make them appealing.

    Add weird text, images, and other elements to make the website more interesting.

    Do not include: ```html ``` - just return the pure html

    """


    html_agent = Agent(
        client=client,
        model=model,
        system_message=system_message,
        tools=[],
        tool_map={},
        max_steps=10
    )
    return html_agent