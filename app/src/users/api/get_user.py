from app.utils.exceptions import CustomException
from app.utils.logger import get_logger
from fastapi import APIRouter,Depends
from app.models.schemas.users.response import CreateGetOrUpdateUserResponse
from app.database.session import get_db
from app.models.domain.users import User
from fastapi import Path
logger = get_logger(__name__)
router = APIRouter()


@router.get(
    path="/user/{user_id}",
    summary="Lista un usuario",
    response_model=CreateGetOrUpdateUserResponse,
    tags=["users"],
    operation_id="cl.kanri.usuarios.obtener"
)
def get_user(db=Depends(get_db), user_id: str = Path(...)):
    user: User = db.query(User).filter(User.userId == user_id).first()
    if not user:
        raise CustomException(name="ErrorListarUsuario", message="Hubo un problema al listar el usuario.", status_code=409)
    return CreateGetOrUpdateUserResponse(usuario=user)
