from typing import Optional, Literal, List
from pydantic import Field
from app.models.schemas.filter_params.base_filter_params import BaseFilterParams

class UserFilterParams(BaseFilterParams):
    order_by: Optional[Literal["name", "email", "created_at"]] = Field("nombre", description="Campo para ordenar")
    dni: Optional[str] = Field(None, description="Filtrar por dni")
    email: Optional[str] = Field(None, description="Filtrar por email")
    created_at: Optional[str] = Field(None, description="Filtrar por fecha creacion")