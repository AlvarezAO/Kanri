from fastapi import APIRouter
from functions_app.src.users.api import create_user, get_all_users, get_user


router = APIRouter()

router.include_router(create_user.router, tags=["users"])
router.include_router(get_all_users.router, tags=["users"])
router.include_router(get_user.router, tags=["users"])
