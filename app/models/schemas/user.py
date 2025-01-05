from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.constants.user_constants import UserStatus


class UserBase(BaseModel):
    name: str
    alias: Optional[str] = None
    dni: str
    email: EmailStr
    phone_number: str = Field(..., alias="phoneNumber")
    phone_number_alternative: Optional[str] = Field(None, alias="phoneNumberAlternative")
    avatar: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    alias: Optional[str] = None
    dni: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, alias="phoneNumber")
    phone_number_alternative: Optional[str] = Field(None, alias="phoneNumberAlternative")
    avatar: Optional[str] = None
    password: Optional[str] = None
    web_access: Optional[bool] = Field(None, alias="webAccess")
    change_password: Optional[bool] = Field(None, alias="changePassword")
    user_status: Optional[UserStatus] = Field(None, alias="userStatus")

    class Config:
        from_attributes = True
        populate_by_name = True
        use_enum_values = True


class UserRead(UserBase):
    user_id: str = Field(..., alias="userId")
    change_password: bool = Field(..., alias="changePassword")
    last_access_date: Optional[datetime] = Field(None, alias="lastAccessDate")
    user_status: UserStatus = Field(..., alias="userStatus")
    web_access: bool = Field(..., alias="webAccess")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")
    failed_login_attempts: int = Field(..., alias="failedLoginAttempts")

    class Config:
        from_attributes = True
        populate_by_name = True
        use_enum_values = True


class UserInDB(UserBase):
    user_id: str = Field(..., alias="userId")
    password: str
    web_access: bool = Field(..., alias="webAccess")
    change_password: bool = Field(..., alias="changePassword")
    user_status: UserStatus = Field(..., alias="userStatus")
    failed_login_attempts: int = Field(..., alias="failedLoginAttempts")

    class Config:
        from_attributes = True
        populate_by_name = True
        use_enum_values = True


class UserResponse(UserBase):
    user_id: str
    user_status: UserStatus = Field(..., alias="userStatus")

    class Config:
        from_attributes = True
        populate_by_name = True
        use_enum_values = True
