from sqlalchemy import Column, String, Integer, DateTime, Boolean, func
from app.database.database import Base
from sqlalchemy.types import Enum
from app.models.constants.user_constants import UserStatus


class User(Base):
    __tablename__ = "users"

    user_id = Column(String(36), primary_key=True)
    name = Column(String(100))
    alias = Column(String(100))
    dni = Column(String(16), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    phone_number = Column("phone_number", String(20))
    phone_number_alternative = Column("phone_number_alternative", String(20))
    password = Column(String(256))
    change_password = Column("change_password", Boolean, default=True)
    last_access_date = Column("last_access_date", DateTime)
    user_status = Column("user_status", Enum(UserStatus), default=UserStatus.ACTIVE)
    web_access = Column("web_access", Boolean, default=True)
    created_at = Column("created_at", DateTime, server_default=func.now())
    updated_at = Column("updated_at", DateTime, onupdate=func.now())
    avatar = Column(String(300))
    failed_login_attempts = Column("failed_login_attempts", Integer)
