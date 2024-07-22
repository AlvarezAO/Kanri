from app.models.domain.users import User


def get_user_by_dni_or_id(value: str, db) -> User:
    user: User = db.query(User).filter(User.dni == value or User.userId == value).first()
    print(f"Usuario encontrado: {user}")
    return user

