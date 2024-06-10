from datetime import datetime
from pydantic import BaseModel
from typing import TypeVar

T = TypeVar('T')


class StandardResponse(BaseModel):
    message: str = "Operación exitosa."
    state: str = "OK"
    statusCode: int = 200
    date: datetime = datetime.now().isoformat()
