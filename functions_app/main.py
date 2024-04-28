import json
from starlette.responses import Response
from urllib.request import Request
from fastapi import FastAPI
from mangum import Mangum
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from functions_app.api.v1.main_router import router as api_router
from datetime import datetime
import time
from functions_app.utils.logger import get_logger
from functions_app.utils.exceptions import CustomException
logger = get_logger(__name__)
app = FastAPI(
    title="Kanri Project API",
    description="FastAPI with AWS Lambda",
    version="0.0.1",
    docs_url="/"
)


@app.middleware("http")
async def custom_error_handler(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
    except CustomException as e:
        process_time = time.time() - start_time
        return JSONResponse(
            status_code=e.status_code,
            content={
                "message": e.message,
                "state": "Error",
                "status_code": e.status_code,
                "date": datetime.now().isoformat(),
                "error_name": e.name,
                "process_time": process_time,
            },
        )


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response: Response = await call_next(request)
        process_time = time.time() - start_time
        print(f"Tiempo de procesamiento: {process_time} segundos")
        response.headers["X-Process-Time"] = str(process_time)
        return response


app.include_router(api_router, prefix="/v1")
app.add_middleware(ProcessTimeMiddleware)
handler = Mangum(app)
