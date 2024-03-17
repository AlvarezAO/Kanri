from fastapi import APIRouter
from functions_app.api.v1.endpoints.users.id import user_get

router = APIRouter()
router.include_router(user_get.router, tags=["users"])
