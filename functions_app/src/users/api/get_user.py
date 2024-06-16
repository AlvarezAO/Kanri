from functions_app.utils.exceptions import CustomException
from functions_app.utils.logger import get_logger
from fastapi import APIRouter,Depends
from functions_app.schemas.users.response import CreateGetOrUpdateUserResponse
from functions_app.database.session import get_db
from functions_app.models.users import User
from fastapi import Path
logger = get_logger(__name__)
router = APIRouter()


@router.get(path="/user/{user_id}", summary="Lista un usuario",
            response_model=CreateGetOrUpdateUserResponse)
def get_user(db=Depends(get_db), user_id: str = Path(...)):
    user: User = db.query(User).filter(User.userId == user_id).first()
    if not user:
        raise CustomException(name="ErrorListarUsuario", message="Hubo un problema al listar el usuario.", status_code=409)
    return CreateGetOrUpdateUserResponse(usuario=user)
