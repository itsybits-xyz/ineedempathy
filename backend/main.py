import sentry_sdk
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
from sentry_asgi import SentryMiddleware

sentry_sdk.init(
    "https://2147b3c92a9b482eaefc19feaeda5ecd@o948279.ingest.sentry.io/5897486",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)

app = FastAPI()
app.include_router(api_router, prefix="/api")
app.mount("/static", StaticFiles(directory="templates/static"), name="static")
app.mount("/api/static", StaticFiles(directory="static"), name="static")
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
app.add_middleware(SentryMiddleware)

@app.get("/{full_path:path}")
async def catch_all(request: Request, full_path: str):
    print("full_path: " + full_path)
    return templates.TemplateResponse("index.html", {"request": request})
