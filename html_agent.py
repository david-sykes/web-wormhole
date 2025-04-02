from agent import Agent
from openai import OpenAI
import os
from tools import image_tool

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

    Always include one image by using the image tool and including the returned path in the html.

    """

    tools = [{
    "type": "function",
    "function": {
        "name": "image_tool",
        "description": "Generate an image from a text prompt and save it to a local path.",
        "parameters": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "A descriptive text prompt to generate the image, e.g., 'A futuristic cityscape at sunset'."
                }
            },
            "required": [
                "prompt"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
    }]

    tool_map = {"image_tool": image_tool}

    html_agent = Agent(
        client=client,
        model=model,
        system_message=system_message,
        tools=tools,
        tool_map=tool_map,
        max_steps=10
    )
    return html_agent