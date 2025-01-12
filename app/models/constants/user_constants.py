from enum import Enum


class UserStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    BANNED = "BANNED"


class WebAccess(Enum):
    GRANTED = True
    REJECTED = False


class ChangePass(Enum):
    YES = True
    NO = False
