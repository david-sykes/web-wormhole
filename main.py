from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from html_agent import html_agent
import uvicorn


app = FastAPI()

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(request: Request, path: str):
    # Get request information
    method = request.method
    url = str(request.url)
    headers = dict(request.headers)

    
    
    # Create a summary of the request
    request_info = f"Method: {method}, Path: /{path}, URL: {url}"

    completion, completion_type, message = html_agent(request_info)
    response_html = completion.message.content
    
    return HTMLResponse(content=response_html)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
