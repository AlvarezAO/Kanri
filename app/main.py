from fastapi import FastAPI
from app.core.config import settings
from app.api.main_router import router as api_router

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    docs_url=settings.DOCS_URL,
    debug=settings.DEBUG
)

app.include_router(api_router)
