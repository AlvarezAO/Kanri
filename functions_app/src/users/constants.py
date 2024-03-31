from enum import Enum as PyEnum


class UserStatus(PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"


class BoolStateYesOrNo(PyEnum):
    YES = True
    NO = False
