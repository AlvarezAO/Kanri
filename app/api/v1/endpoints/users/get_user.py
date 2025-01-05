import time
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.schemas.user import UserResponse
from app.models.schemas.response_model import ResponseModel
from app.services.user_services import UserService
from app.api.dependencies import get_db

router = APIRouter()


@router.get(
    path="/users/{user_id}",
    summary="List a user",
    response_model=ResponseModel[UserResponse],
    tags=["Users"],
    operation_id="cl.kanri.usuarios.obtener"
)
def get_user(user_id: str,  db: Session = Depends(get_db)) -> ResponseModel[UserResponse]:
    start_time = time.perf_counter()
    user_service = UserService(db)
    user = user_service.get_user(user_id)
    end_time = time.perf_counter()
    execution_time = end_time - start_time

    return ResponseModel(
        ejecucion=execution_time,
        mensaje="Usuario listado correctamente",
        data=user
    )