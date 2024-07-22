from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from app.database.session import get_db
from datetime import timedelta
from app.services.security.auth import AuthHandler
from app.src.auth.services import authenticate_user, hash_password, create_access_token
from app.utils.logger import get_logger
from app.models.schemas.token.base import Token, ACCESS_TOKEN_EXPIRE_MINUTES


logger = get_logger(__name__)
router = APIRouter()
auth_handle = AuthHandler()


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_handle.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await auth_handle.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
