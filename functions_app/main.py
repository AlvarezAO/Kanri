from fastapi import FastAPI
from mangum import Mangum
from functions_app.api.v1.main_router import router as api_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Kanri Project API",
    description="FastAPI with AWS Lambda",
    version="0.0.1",
    docs_url="/"
)

app.include_router(api_router, prefix="/v1")

handler = Mangum(app)
