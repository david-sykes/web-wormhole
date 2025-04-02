from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from html_agent import initialise_html_agent
import uvicorn
import os

app = FastAPI()

# Mount the static directory
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(request: Request, path: str):
    # Get request information
    method = request.method
    url = str(request.url)
    headers = dict(request.headers)

    
    html_agent = initialise_html_agent()
    # Create a summary of the request
    request_info = f"Method: {method}, Path: /{path}, URL: {url}"

    content = html_agent.run_agent_loop(request_info)
    response_html = content
    
    return HTMLResponse(content=response_html)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
