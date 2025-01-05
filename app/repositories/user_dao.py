import uuid

from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from app.models.domain.user import User
from app.models.schemas.user import UserBase, UserUpdate
from app.models.constants.user_constants import UserStatus, WebAccess, ChangePass
from app.models.schemas.filter_params.user_filter_params import UserFilterParams
from app.models.schemas.user import UserRead
from typing import List, Tuple
from uuid import uuid4


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: str):
        return self.db.query(User).filter(User.user_id == user_id).first()

    def get_by_dni(self, dni: str):
        dni_formatted = dni.replace(".", "")
        user = self.db.query(User).filter(User.dni == dni_formatted).first()
        return user

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user: UserBase, hashed_password: str):
        #agregar un try/catch al crear
        db_user = User(
            user_id=str(uuid4()),
            name=user.name,
            alias=user.alias,
            dni=user.dni,
            email=user.email,
            phone_number=user.phone_number,
            phone_number_alternative=user.phone_number_alternative,
            password=hashed_password,
            change_password=ChangePass.YES.value,
            user_status=UserStatus.ACTIVE,
            web_access=WebAccess.GRANTED.value,
            created_at=func.now(),
            avatar=user.avatar,
            failed_login_attempts=0
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user


    def get_users_with_filters(self, params: UserFilterParams) -> Tuple[List[UserRead], int]:
        query = self.db.query(User)

        # Aplicar filtros específicos
        if params.dni:
            query = query.filter(User.dni.ilike(f"%{params.dni}%"))
        if params.email:
            query = query.filter(User.email.ilike(f"%{params.email}%"))
        if params.created_at:
            query = query.filter(User.created_at == params.created_at)

        # Obtener total de elementos antes de paginar
        total_items = query.count()

        # Aplicar ordenamiento
        if params.order_by:
            order_field = getattr(User, params.order_by)
            if params.order_direction == "desc":
                query = query.order_by(order_field.desc())
            else:
                query = query.order_by(order_field.asc())

        # Aplicar paginación
        query = query.offset((params.page - 1) * params.size).limit(params.size)

        users = query.all()
        # Convertir a esquemas Pydantic
        users_read = [UserRead.model_validate(user) for user in users]

        return users_read, total_items


    def delete_user(self, user_id: str):
        #Validar que sea de la misma empresa?
        # Porque un usuario podria ir a mas de una sucursal o empresa de distinta area
        return
