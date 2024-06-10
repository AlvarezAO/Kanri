from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from functions_app.src.users.constants import UserStatus


class UserCreate(BaseModel):
    name: str
    alias: str
    dni: str
    email: str
    phoneNumber: str
    phoneNumberAlternative: Optional[str] = Field(None)
    avatar: Optional[str] = Field(None)
    class Config:
        from_attributes = True


class UserUpdate(UserCreate):
    password: str
    webAccess: bool

class UserRead(UserCreate):
    userId: str
    changePassword: bool
    lastAccessDate: Optional[datetime]
    userStatus: UserStatus
    createdAt: datetime
    updatedAt: Optional[datetime]
    failedLoginAttempts: int

    class Config:
        from_attributes = True

class UserDB(UserRead):
    password: str
    webAccess: bool
