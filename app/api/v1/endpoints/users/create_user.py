from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.schemas.user import UserBase, UserResponse
from app.models.schemas.response_model import ResponseModel
from app.services.user_services import UserService
from app.api.dependencies import get_db

router = APIRouter()


@router.post(
    path="/users",
    summary="Crear Usuario",
    response_model=ResponseModel[UserResponse],
    description="Crear usuario dentro del sistema",
    tags=["Users"],
    operation_id="cl.kanri.usuarios.crear"
)
def create_user(user: UserBase, db: Session = Depends(get_db)) -> ResponseModel[UserResponse]:
    user_service = UserService(db)
    existing_user_by_dni = user_service.user_repository.get_by_dni(user.dni)
    existing_user_by_email = user_service.user_repository.get_by_email(user.email)

    if existing_user_by_dni:
        raise HTTPException(status_code=400, detail="El RUT ya está registrado")
    if existing_user_by_email:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")

    user = user_service.create_user(user)
    return ResponseModel(data=user)

