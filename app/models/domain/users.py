from sqlalchemy import Column, String, Integer, DateTime, Boolean, func
from app.database.session import Base
from sqlalchemy.types import Enum
from app.services.constants.user_status import UserStatus


class User(Base):
    __tablename__ = "users"

    userId = Column("user_id", String(36), primary_key=True)
    name = Column(String(100))
    alias = Column(String(100))
    dni = Column(String(16), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    phoneNumber = Column("phone_number", String(20))
    phoneNumberAlternative = Column("phone_number_alternative", String(20))
    password = Column(String(256))
    changePassword = Column("change_password", Boolean, default=True)
    lastAccessDate = Column("last_access_date", DateTime)
    userStatus = Column("user_status", Enum(UserStatus))
    webAccess = Column("web_access", Boolean, default=True)
    createdAt = Column("created_at", DateTime, server_default=func.now())
    updatedAt = Column("updated_at", DateTime, onupdate=func.now())
    avatar = Column(String(300))
    failedLoginAttempts = Column("failed_login_attempts", Integer)
