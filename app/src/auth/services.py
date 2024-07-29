import secrets
import string
from typing import Optional
from bcrypt import gensalt, hashpw, checkpw
import base64
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from app.database.dao.users import get_user_by_dni_or_id
from app.models.domain.users import User
from app.models.schemas.token.base import TokenData, SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer("/login")


def hash_password(password: str) -> str:
    salt = gensalt()
    hashed = hashpw(password.encode('utf-8'), salt)
    return base64.b64encode(hashed).decode('utf-8')  # Codifica en base64 para almacenar como string


def verify_password(stored_hash: str, provided_password: str) -> bool:
    stored_hash_bytes = base64.b64decode(stored_hash.encode('utf-8'))  # Decodifica de base64 a bytes
    provided_password_bytes = provided_password.encode('utf-8')
    return checkpw(provided_password_bytes, stored_hash_bytes)


def generate_secure_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data


def authenticate_user(username: str, password: str, db):
    user = get_user_by_dni_or_id(username, db)
    if not user:
        return False
    if not verify_password(user.password, password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    # Aquí debes reemplazar la función get_user con tu lógica de obtención de usuario
    user = User.select(User.dni == username).first()
    if user is None:
        raise credentials_exception
    return user