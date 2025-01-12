from typing import TypeVar, Generic, Optional, List
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timezone

DataT = TypeVar('DataT')

class PaginationMeta(BaseModel):
    page: int
    size: int
    total: int
    total_pages: int

class ResponseModel(BaseModel, Generic[DataT]):
    estado: str = Field(default="ok")
    fecha: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ejecucion: Optional[float] = None
    mensaje: Optional[str] = Field(default="Operación exitosa")
    codigo: int = Field(default=200)
    data: Optional[DataT] = None
    meta: Optional[PaginationMeta] = None

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )