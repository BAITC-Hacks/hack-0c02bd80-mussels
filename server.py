from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from services.storage import Storage
from services.ai_generator import AIGenerator

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

STATIC_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="AI Sana Web App",
    description="Standalone web application for AI Sana hackathon platform",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

storage = Storage()
ai_generator = AIGenerator()


def get_ai_status() -> str:
    return "OpenAI API" if ai_generator.client else "Локальный движок"


@app.api_route("/", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "current_route": "/",
            "ai_status": get_ai_status(),
        }
    )


@app.api_route("/catalog", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def catalog_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="catalog.html",
        context={
            "current_route": "/catalog",
            "ai_status": get_ai_status(),
        }
    )


@app.api_route("/student", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def student_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="student.html",
        context={
            "current_route": "/student",
            "ai_status": get_ai_status(),
        }
    )


@app.api_route("/business", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def business_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="business.html",
        context={
            "current_route": "/business",
            "ai_status": get_ai_status(),
        }
    )


@app.api_route("/jury-demo", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def jury_demo_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="jury_demo.html",
        context={
            "current_route": "/jury-demo",
            "ai_status": get_ai_status(),
        }
    )


@app.get("/demo")
async def demo_redirect():
    return RedirectResponse(url="/jury-demo", status_code=302)


@app.post("/api/reset-data")
async def reset_data_endpoint():
    storage.reset_all_data()
    return JSONResponse(
        {
            "status": "ok",
            "message": "База данных успешно сброшена к начальному эталонному состоянию"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
