from datetime import datetime
from pydantic import BaseModel, validator
from typing import Generic, TypeVar, Optional
from pydantic.generics import GenericModel

T = TypeVar('T')


class StandardResponse(BaseModel):
    message: str = "Operación exitosa."
    state: str = "OK"
    statusCode: int = 200
    date: datetime = datetime.now().isoformat()
