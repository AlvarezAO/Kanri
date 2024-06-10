from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from functions_app.models.users import User
from functions_app.database.session import get_db
from functions_app.src.users.api import ALLOWED_FILTER_FIELDS
from functions_app.src.users.constants import UserStatus
from functions_app.utils.filters import apply_filters, apply_order
from functions_app.utils.pagination import apply_pagination, calcular_total_paginas
from functions_app.schemas.users.response import GetAllUsersResponse
from sqlalchemy.exc import SQLAlchemyError
from functions_app.utils.logger import get_logger
from functions_app.utils.exceptions import CustomException

#from kanri_app.modules.auth.endpoints.get_token import get_current_active_user

logger = get_logger(__name__)
router = APIRouter()


@router.get(path="/users", summary="Listar Usuarios Registrados",
            description="Obtiene un listado de todos los usuarios registrados y habilitados, con su información.",
            response_model=GetAllUsersResponse)
async def get_users(
    db=Depends(get_db),
    filters: Optional[str] = Query(None),
    items_by_page: Optional[int] = Query(10, gt=0),
    page: Optional[int] = Query(1, gt=0),
    order: Optional[str] = Query(None, example="nombre,asc")
    ):
    
    try:
        query = db.query(User).filter(User.userStatus == UserStatus.ACTIVE.value)
        allowed_fields = ALLOWED_FILTER_FIELDS.get('User', [])
        query = apply_filters(query, User, filters, allowed_fields)
        query = apply_order(query, User, order, allowed_fields)
        total_items = query.count()
        if items_by_page and page:
            query = apply_pagination(query, page, items_by_page)

        users = query.all()
        response = GetAllUsersResponse(
            usuarios=users,
            pagina=page,
            totalElementos=total_items,
            totalPaginas=calcular_total_paginas(total_items, items_by_page),
            mensaje="Usuarios listados correctamente."
        )
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener usuarios: {e}")
        raise CustomException(name="ErrorListarUsuarios", message="Hubo un problema al listar los usuarios.", status_code=409)

    return response
