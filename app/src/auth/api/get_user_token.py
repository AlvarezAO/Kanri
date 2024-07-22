from fastapi import Depends, APIRouter

from app.models.domain.users import User
from app.src.auth.services import get_current_user
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user