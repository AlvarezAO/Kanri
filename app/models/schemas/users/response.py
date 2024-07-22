from typing import List
from app.models.schemas.base_response import StandardResponse
from app.models.schemas.users.base import UserRead


class GetAllUsersResponse(StandardResponse):
    usuarios: List[UserRead]
    pagina: int = 1
    totalElementos: int = 10
    totalPaginas: int = 1


class CreateGetOrUpdateUserResponse(StandardResponse):
    usuario: UserRead
