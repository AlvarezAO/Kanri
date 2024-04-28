from sqlalchemy import Column, String, Integer, DateTime, Boolean, func
from functions_app.database.session import Base
from sqlalchemy.types import Enum
from functions_app.src.users.constants import UserStatus


class User(Base):
    __tablename__ = "users"

    user_id = Column(String(36), primary_key=True)
    name = Column(String(100))
    alias = Column(String(100))
    dni = Column(String(16), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    phone_number = Column(String(20))
    phone_number_alternative = Column(String(20))
    password = Column(String(256))
    change_password = Column(Boolean, default=True)
    last_access_date = Column(DateTime)
    user_status = Column(Enum(UserStatus))
    web_access = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    avatar = Column(String(300))
    failed_login_attempts = Column(Integer)
