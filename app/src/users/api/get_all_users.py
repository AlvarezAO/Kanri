from typing import Optional
from fastapi import APIRouter, Depends, Query

from app.models.domain.users import User
from app.database.session import get_db
from app.services.decoradores.validador_permisos import require_permission
from app.src.users.api import ALLOWED_FILTER_FIELDS
from app.services.constants.user_status import UserStatus
from app.utils.filters import apply_filters, apply_order
from app.utils.pagination import apply_pagination, calcular_total_paginas
from app.models.schemas.users.response import GetAllUsersResponse
from sqlalchemy.exc import SQLAlchemyError
from app.utils.logger import get_logger
from app.utils.exceptions import CustomException
from app.src.auth.services import oauth2_scheme
logger = get_logger(__name__)
router = APIRouter()


@router.get(
    path="/user",
    summary="Listar Usuarios Registrados",
    description="Obtiene un listado de todos los usuarios registrados y habilitados, con su información.",
    response_model=GetAllUsersResponse,
    tags=["users"],
    operation_id="cl.kanri.usuarios.listar"
)
async def get_users(
        db=Depends(get_db),
        filters: Optional[str] = Query(None),
        items_by_page: Optional[int] = Query(10, gt=0),
        page: Optional[int] = Query(1, gt=0),
        order: Optional[str] = Query(None, example="nombre,asc")
):
    logger.info("Entro a la API")
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
        raise (CustomException
               (name="ErrorListarUsuarios",
                message="Hubo un problema al listar los usuarios.",
                status_code=409)
               )

    return response
