import time
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.schemas.user import UserResponse
from app.models.schemas.response_model import ResponseModel, PaginationMeta
from app.services.user_services import UserService
from app.api.dependencies import get_db
from app.models.schemas.filter_params.user_filter_params import UserFilterParams

router = APIRouter()


@router.get(
    path="/users",
    summary="List all users",
    response_model=ResponseModel[List[UserResponse]],
    tags=["Users"],
    operation_id="cl.kanri.usuarios.listar"
)
def get_all_users(params: UserFilterParams = Depends(),  db: Session = Depends(get_db)) -> ResponseModel[List[UserResponse]]:
    start_time = time.perf_counter()
    user_service = UserService(db)
    users, total_items = user_service.get_all_users(params)
    end_time = time.perf_counter()
    execution_time = end_time - start_time

    total_pages = (total_items + params.size - 1) // params.size

    response = ResponseModel(
        ejecucion=execution_time,
        mensaje="Usuarios listados correctamente.",
        data=users,
        meta=PaginationMeta(
            page=params.page,
            size=params.size,
            total=total_items,
            total_pages=total_pages
        )
    )
    return response
