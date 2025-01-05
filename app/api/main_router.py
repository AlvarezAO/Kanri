from fastapi import APIRouter

from app.api.dependencies import get_db
from app.api.v1.endpoints.users import create_user, get_all_users, get_user

router = APIRouter()

router.include_router(create_user.router)
router.include_router(get_all_users.router)
router.include_router(get_user.router)