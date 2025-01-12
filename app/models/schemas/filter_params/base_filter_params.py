from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal

class BaseFilterParams(BaseModel):
    model_config = ConfigDict(extra="forbid")  # Prohíbe parámetros extra

    page: int = Field(1, ge=1, description="Número de página")
    size: int = Field(10, ge=1, le=100, description="Tamaño de página")
    order_by: Optional[str] = Field(None, description="Campo para ordenar")
    order_direction: Literal["asc", "desc"] = Field("asc", description="Dirección de ordenamiento")