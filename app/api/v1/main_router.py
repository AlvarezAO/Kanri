from fastapi import APIRouter
from app.src.users.api import create_user, get_all_users, get_user
from app.src.auth.api import get_token


router = APIRouter()

router.include_router(create_user.router, tags=["users"])
router.include_router(get_all_users.router, tags=["users"])
router.include_router(get_user.router, tags=["users"])
router.include_router(get_token.router, tags=["auth"])
