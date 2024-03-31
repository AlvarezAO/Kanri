from typing import List
from functions_app.schemas.base_response import StandardResponse
from functions_app.schemas.users.base import UserRead


class GetAllUsersResponse(StandardResponse):
    usuarios: List[UserRead]
    pagina: int = 1
    totalElementos: int = 10
    totalPaginas: int = 1


class CreateGetOrUpdateUserResponse(StandardResponse):
    usuario: UserRead
