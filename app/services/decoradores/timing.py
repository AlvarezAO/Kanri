from datetime import datetime
from typing import Callable
from fastapi import FastAPI, Request
import json
from fastapi.responses import JSONResponse


def timing_decorator(api_func: Callable):
    async def wrapper(*args, **kwargs):
        start_time = datetime.now()
        response = await api_func(*args, **kwargs)
        end_time = datetime.now()
        process_time = (end_time - start_time).total_seconds()

        if isinstance(response, JSONResponse):
            content = response.body.decode()
            response_body = json.loads(content)
            response_body['process_time'] = process_time
            response.body = json.dumps(response_body).encode('utf-8')
        else:
            response['process_time'] = process_time

        return response
    return wrapper
