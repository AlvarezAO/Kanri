import json
from starlette.responses import Response
from urllib.request import Request
from fastapi import FastAPI
from mangum import Mangum
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.api.v1.main_router import router as api_router
from datetime import datetime
import time
from app.utils.logger import get_logger
from app.utils.exceptions import CustomException
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
        response: Response = await call_next(request)
        process_time = time.time() - start_time
        formatted_process_time = "{:.3f}".format(process_time)

        # Verifica si la respuesta es de tipo JSON
        if response.media_type == "application/json":
            content = await response.body()
            content = json.loads(content)
            content["process_time"] = formatted_process_time
            content["date"] = datetime.now().isoformat()
            return JSONResponse(status_code=response.status_code, content=content)

        # Para otros tipos de respuesta, simplemente añade el encabezado
        response.headers["X-Process-Time"] = str(formatted_process_time)
        return response

    except CustomException as e:
        process_time = time.time() - start_time
        formatted_process_time = "{:.3f}".format(process_time)
        return JSONResponse(
            status_code=e.status_code,
            content={
                "message": e.message,
                "state": "Error",
                "status_code": e.status_code,
                "date": datetime.now().isoformat(),
                "error_name": e.name,
                "process_time": formatted_process_time,
            },
        )
    finally:
        process_time = time.time() - start_time
        formatted_process_time = "{:.3f}".format(process_time)
        logger.info(f"Tiempo de procesamiento: {formatted_process_time} segundos")


app.include_router(api_router)
handler = Mangum(app)
