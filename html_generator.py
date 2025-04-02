from tools import image_tool, canvas_physics_animation, strip_code_fence, Image, Canvas
from openai import OpenAI
import os
import json
from pydantic import BaseModel


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])



class HTMLResponse(BaseModel):
    html: str
    images: list[Image]
    canvas: list[Canvas]




def generate_html_framework(prompt: str):
    system_prompt = """
    You are a website generator. You will be given a prompt and you should return an html file with a website that can be included in an html file.
    
    <INSTRUCTIONS>
    - Include placeholders for 1 image. Include the image name and description in the structured output. Images are stored at /static/img/
    - Include placeholders for 1 canvas element. Include the canvas name and description in the structured output. Canvas is stored at /static/js/
    - Make links in your website that might have weird paths for further generation
    - Give the websites structure, styling and animations
    - Always use a grid layout to give the website more structure
    - Add a nice amount of text
    - Add scroll effects
    - Use css styling to make it beautiful and snazzy. Include all the styling in line.
    - Output in json compatible format


    For the canvas element:
    <canvas id="canvas" width="300" height="300"></canvas>

    </INSTRUCTIONS>
    """

    prompt_for_model = f"""
    Make a website about:
    {prompt}
    """
    
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages= [{"role": "system", "content": system_prompt}, 
        {"role": "user", "content": prompt_for_model}
        ],
        response_format=HTMLResponse
    )
    

    output = completion.choices[0].message.content
    print(output)

    output = json.loads(output)

    html = output.get("html", "")
    images = output.get("images", [])
    canvas = output.get("canvas", [])

    return html, images, canvas


if __name__ == "__main__":
    html, images, canvas = generate_html_framework("a cat")
    populate_html_with_content(html, images, canvas)
