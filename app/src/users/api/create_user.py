from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy import or_
from app.services.decoradores.timing import timing_decorator
from app.utils.exceptions import CustomException
from app.models.schemas.users.base import UserCreate
from app.models.domain.users import User
from app.src.auth.services import hash_password, generate_secure_password
from app.services.constants.user_status import UserStatus
from app.database.session import get_db
from app.models.schemas.users.response import CreateGetOrUpdateUserResponse
from app.services.security.auth import AuthHandler
from sqlalchemy.exc import SQLAlchemyError
from app.utils.logger import get_logger
from sqlalchemy.orm import Session
from uuid import uuid4

logger = get_logger(__name__)

router = APIRouter()
auth = AuthHandler()


@timing_decorator
@router.post(
    path="/user",
    summary="Crear Usuario",
    description="Crea usuario en los registros del sistema",
    tags=["users"],
    operation_id="cl.kanri.usuarios.crear"
)
async def post_user(user: UserCreate, db=Depends(get_db)) -> CreateGetOrUpdateUserResponse:
    if valida_existencia_usuario(user, db):
        raise CustomException(name="UsuarioExistente", message="El usuario ya existe en nuestros registros.", status_code=409)
    db_user = create_user(user)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return CreateGetOrUpdateUserResponse(usuario=db_user)
    except SQLAlchemyError as e:
        logger.error(f"Error al crear usuario: {e}")
        raise CustomException(name="ErrorUsuario", message="Hubo un problema al crear el usuario.", status_code=409)


def create_user(user: UserCreate) -> User:
    secure_password = generate_secure_password()
    logger.info(f"Contraseña creada: {secure_password}")
    hashed_password = auth.get_password_hash(secure_password)
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
