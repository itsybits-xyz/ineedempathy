from fastapi.staticfiles import StaticFiles
from fastapi import (
    Request,
    FastAPI,
)
from fastapi.middleware.cors import CORSMiddleware
from .middleware import ConnectionManagerMiddleware
from .config import settings
from .routers.api import router as api_router
from fastapi.templating import Jinja2Templates


app = FastAPI()
app.include_router(api_router, prefix="/api")
app.mount("/static", StaticFiles(directory="templates/static"), name="static")
app.mount("/api/static", StaticFiles(directory="backend/static"), name="static")
templates = Jinja2Templates(directory="templates")

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

app.add_middleware(ConnectionManagerMiddleware)


@app.get("/{full_path:path}")
async def catch_all(request: Request, full_path: str):
    print("full_path: " + full_path)
    return templates.TemplateResponse("index.html", {"request": request})
