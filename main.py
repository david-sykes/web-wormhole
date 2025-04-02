from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from html_generator import generate_html_framework
from tools import image_tool, canvas_physics_animation
import uvicorn
import os

app = FastAPI()

static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

generated_pages = {}
locks = {}

def generate_page(path: str):
    request_info = f"Generated content for /{path}"
    html, images, canvas = generate_html_framework(request_info)

    for image in images:
        image_tool(image['description'], image['filename'])
    for c in canvas:
        canvas_physics_animation(c['description'], c['filename'])

    generated_pages[path] = html

@app.get("/status/{path:path}")
async def status(path: str):
    return JSONResponse({"ready": path in generated_pages})

@app.get("/result/{path:path}")
async def result(path: str):
    if path in generated_pages:
        return HTMLResponse(content=generated_pages[path])
    return HTMLResponse("Not ready yet", status_code=404)

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(request: Request, path: str, background_tasks: BackgroundTasks):
    if path not in generated_pages:
        background_tasks.add_task(generate_page, path)
    return FileResponse(os.path.join(static_dir, "html","loading.html"))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
