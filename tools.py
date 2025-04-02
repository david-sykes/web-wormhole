from openai import OpenAI
import os
import requests
import uuid
import re
import json
from pydantic import BaseModel

class Image(BaseModel):
    filename: str
    description: str

class Canvas(BaseModel):
    filename: str
    description: str
    javascript: str

def image_tool(prompt: str, filename: str):
    """Takes a prompt, generates an image and saves it to a path.
    Returns the path """
    # Generate a unique filename using UUID
    path = os.path.join('static/img', filename)
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.images.generate(
        model="dall-e-2",
        prompt=prompt,
        size="256x256",
        quality="standard",
        n=1)
    print(response.data[0].url)
    # Download the image and save to static/img folder
    image = requests.get(response.data[0].url)
    with open(path, 'wb') as f:
        f.write(image.content)
    return path

def strip_code_fence(text: str) -> str:
    # Match optional code fence with optional language identifier at the start and end
    code_fence_pattern = r"^```(?:\w+)?\n(.*?)\n```$"
    match = re.match(code_fence_pattern, text.strip(), re.DOTALL)
    if match:
        return match.group(1)
    return text.strip()

def canvas_physics_animation(prompt: str, filename: str):
    """Takes a prompt, generate a js file with a physics animation canvas element that can be included in an html file"""
    # Generate a unique filename using UUID
    system_prompt = """
    You are a physics animation canvas element generator. You will be given a prompt and you should return a js file with a physics animation canvas element that can be included in an html file.
    Return a json object with filename, description and javascript code.
    """
    hydrated_prompt = f"""
    Make the animation about: {prompt}
    Filename: {filename}
    """
    path = os.path.join('static/js', filename)
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages= [{"role": "system", "content": system_prompt}, 
            {"role": "user", "content": hydrated_prompt}
            ],
            response_format = Canvas
        )
    output = json.loads(completion.choices[0].message.content)
    js = output['javascript']

    # Download the image and save to static/img folder
    with open(path, 'w') as f:
        f.write(js)
    return path

if __name__ == "__main__":
    canvas_physics_animation("a ball", 'test.js')
    # image_tool("cartoon cat")
