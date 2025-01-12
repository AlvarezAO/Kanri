from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.schemas.user import UserBase, UserResponse
from app.models.schemas.response_model import ResponseModel
from app.services.user_services import UserService
from app.api.dependencies import get_db

router = APIRouter()


@router.delete(
    path="/users/{user_id}",
    summary="Eliminar Usuario",
    response_model=ResponseModel[UserResponse],
    description="Elimina usuario dentro del sistema",
    tags=["Users"],
    operation_id="cl.kanri.usuarios.eliminar"
)
def delete_user():
    print("Eliminar Usuario")
    return "ok"
