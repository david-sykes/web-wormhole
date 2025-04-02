from openai import OpenAI
import os
import requests
import uuid

def image_tool(prompt: str):
    """Takes a prompt, generates an image and saves it to a path.
    Returns the path """
    # Generate a unique filename using UUID
    filename = f"{uuid.uuid4()}.jpg"
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

if __name__ == "__main__":
    image_tool("cartoon cat")
