from fastapi import APIRouter
from functions_app.src.users.api import create_user


router = APIRouter()

router.include_router(create_user.router, tags=["users"])
