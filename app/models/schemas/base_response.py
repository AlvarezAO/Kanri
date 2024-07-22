from datetime import datetime
from pydantic import BaseModel
from typing import TypeVar

T = TypeVar('T')


class StandardResponse(BaseModel):
    mensaje: str = "Operación exitosa."
    estado: str = "OK"
    codigo: int = 200
    fecha: datetime = datetime.now().isoformat()
