from sqlalchemy.orm import Session

from app.models.schemas.filter_params.user_filter_params import UserFilterParams
from app.repositories.user_dao import UserRepository
from app.models.schemas.user import UserBase, UserUpdate
from app.utils.security import get_password_hash, verify_password, generate_secure_password


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def get_user(self, user_id: str):
        return self.user_repository.get_by_id(user_id)

    def create_user(self, user: UserBase):
        password = generate_secure_password(16)
        hashed_password = get_password_hash(password)
        print(f"Clave Generada: {password}")
        return self.user_repository.create(user, hashed_password)

    def get_all_users(self, params: UserFilterParams):
        return self.user_repository.get_users_with_filters(params)
