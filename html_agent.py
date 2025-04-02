from agent import Agent
from openai import OpenAI
import os
from tools import image_tool, canvas_physics_animation

### THIS FILE IS NO LONGER USED

def initialise_html_agent():
    client  = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = "gpt-4o"

    system_message = """
    You are an infinite website generating app. You will be given http requests and you should return html responses.

    ONLY RETURN THE HTML

    You should create weird and wacky websites with links to other websites on the same path. Intepret the type of website from the path you are 
    originally passed.

    <STYLE GUIDE>

    - Make links in your website that might have weird paths for further generation. 

    - Give the websites structure, styling, animations, canvases and interactivity. Make them appealing.

    - Always use a grid layout to give the website more structure.

    - Add a nice amount of text
    
    - Always include at least one image by using the image tool and including the returned path in the html.

    - Add scroll effects

    - Use css styling to make it beautiful and snazzy
    
    - Do not include: ```html ``` - just return the pure html

    - Add canvas elemnts and css animated backgrounds

    - Always include an html canvas element with id="canvas"

    - Use the canvas_physics_animation tool to add physics animations to the canvas. 
    Include the path for the javascript file provided by the tool.
    
    </STYLE GUIDE>


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
    }},
    {
    "type": "function",
    "function": {
        "name": "canvas_physics_animation",
        "description": "Generate a JavaScript file with a canvas-based physics animation based on a prompt. The file can be embedded in an HTML page.",
        "parameters": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "A natural language description of the desired physics animation, e.g., 'bouncing balls under gravity'."
                }
            },
            "required": [
                "prompt"
            ],
            "additionalProperties": False
        },
        "strict": True
    }}]

    tool_map = {"image_tool": image_tool, "canvas_physics_animation": canvas_physics_animation}

    html_agent = Agent(
        client=client,
        model=model,
        system_message=system_message,
        tools=tools,
        tool_map=tool_map,
        max_steps=10
    )
    return html_agent