from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy import or_
from functions_app.core.decoradores.timing import timing_decorator
from functions_app.utils.exceptions import CustomException
from functions_app.schemas.users.base import UserCreate
from functions_app.models.users import User
from functions_app.src.auth.services import hash_password, generate_secure_password
from functions_app.src.users.constants import UserStatus
from functions_app.database.session import get_db
from functions_app.schemas.users.response import CreateGetOrUpdateUserResponse
#from kanri_app.modules.auth.endpoints.get_token import get_current_active_user
from sqlalchemy.exc import SQLAlchemyError
from functions_app.utils.logger import get_logger
from sqlalchemy.orm import Session
from uuid import uuid4

logger = get_logger(__name__)

router = APIRouter()


@timing_decorator
@router.post(path="/users", summary="Crear Usuario", description="Crea usuario en los registros del sistema")
async def post_user(user: UserCreate, db=Depends(get_db)) -> CreateGetOrUpdateUserResponse:
    if valida_existencia_usuario(user, db):
        raise CustomException(
            name="UsuarioExistente",
            message="El usuario ya existe en nuestros registros.",
            status_code=409
        )
    db_user = create_user(user)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return CreateGetOrUpdateUserResponse(
            usuario=db_user
        )
    except SQLAlchemyError as e:
        logger.error(f"Error al crear usuario: {e}")
        raise CustomException(name="ErrorUsuario", message="Hubo un problema al crear el usuario.", status_code=409)


def create_user(user: UserCreate) -> User:
    secure_password = generate_secure_password()
    logger.info(f"Contraseña creada: {secure_password}")
    hashed_password = hash_password(secure_password)
    try:
        db_user = User(
            userId=str(uuid4()),
            name=user.name,
            alias=user.alias,
            dni=user.dni,
            email=user.email,
            phoneNumber=user.phoneNumber,
            phoneNumberAlternative=user.phoneNumberAlternative if user.phoneNumberAlternative else None,
            avatar=user.avatar if user.avatar else None,
            changePassword=False,  # Se deja en NO, por ahora hasta implementar correo y vista
            createdAt=datetime.now(),
            failedLoginAttempts=0,
            userStatus=UserStatus.ACTIVE.value,
            webAccess=True,
            password=hashed_password
        )
        return db_user
    except Exception as e:
        logger.error(f"Error al crear usuario: {e}")
        raise CustomException(name="Error", message=f"Error con un dato: {e}", status_code=409)


def valida_existencia_usuario(user: UserCreate, db: Session) -> bool:
    rut_formateado = user.dni.replace(".", "")
    email = user.email
    user_found = db.query(User).filter(or_(User.dni == rut_formateado, User.email == email)).first()
    return user_found is not None
