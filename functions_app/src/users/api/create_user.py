from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from functions_app.schemas.users.base import UserCreate, UserRead
from functions_app.models.users import User
from functions_app.src.auth.services import hash_password, generate_secure_password
from functions_app.src.users.constants import UserStatus, BoolStateYesOrNo
from functions_app.database.session import get_db
from functions_app.schemas.users.response import CreateGetOrUpdateUserResponse
#from kanri_app.modules.auth.endpoints.get_token import get_current_active_user
from sqlalchemy.exc import SQLAlchemyError
from functions_app.utils.logger import get_logger
from sqlalchemy.orm import Session
from uuid import uuid4

logger = get_logger(__name__)

router = APIRouter()


@router.post(path="/users",
             summary="Crear Usuario",
             description="Crea usuario en los registros del sistema",
             response_model=CreateGetOrUpdateUserResponse)
async def post_user(user: UserCreate, db=Depends(get_db)) -> CreateGetOrUpdateUserResponse:
    if not valida_existencia_usuario(user, db):
        db_user = create_user(db, user)
        # TODO enviar un email al correo de usuario registrado, con la clave predeterminada para que la actualice
        # template armarlo con jinja, y ver como enviar correos y guardar registros de estos.
        return CreateGetOrUpdateUserResponse(mensaje="Usuario ha sido creado exitosamente.",
                                             usuario=db_user)
    else:
        return CreateGetOrUpdateUserResponse(mensaje="Error al crear el usuario.",
                                             codigo=409,
                                             estado="Error")


def create_user(db: Session, user: UserCreate) -> UserRead:
    secure_password = generate_secure_password()
    logger.info(f"Contraseña creada: {secure_password}")
    hashed_password = hash_password(secure_password)
    try:
        db_user = User(
            user_id=str(uuid4()),
            name=user.name,
            alias=user.alias,
            dni=user.dni,
            email=user.email,
            phone_number=user.phone_number,
            phone_number_alternative=user.phone_number_alternative if user.phone_number_alternative else None,
            avatar=user.avatar if user.avatar else None,
            change_password=BoolStateYesOrNo.NO.value,  # Se deja en NO, por ahora hasta implementar correo y vista
            created_at=datetime.now(),
            failed_login_attempts=0,
            user_status=UserStatus.ACTIVE,
            web_access=BoolStateYesOrNo.YES.value,
            password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    except SQLAlchemyError as e:
        logger.error(f"Error al crears usuario: {e}")
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error interno al procesar la solicitud."
        )


def valida_existencia_usuario(user: UserCreate, db: Session):
    rut_formateado = user.dni.replace(".", "")
    user = db.query(User).filter(User.dni == rut_formateado or User.email == user.email).first()
    exist = True if user else False
    return exist
