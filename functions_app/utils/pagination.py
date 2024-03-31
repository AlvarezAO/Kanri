from sqlalchemy.orm import Query as SQLAlchemyQuery
from fastapi import HTTPException


# Paginación
def apply_pagination(query: SQLAlchemyQuery, page: int, items_per_page: int) -> SQLAlchemyQuery:
    if page < 1 or items_per_page < 1:
        raise HTTPException(status_code=400, detail="Número de página y elementos por página deben ser positivos")
    return query.offset((page - 1) * items_per_page).limit(items_per_page)


# Calculo Páginas
def calcular_total_paginas(total_items: int, items_por_pagina: int) -> int:
    if items_por_pagina is None or items_por_pagina <= 0:
        return 1
    return -(-total_items // items_por_pagina)  # Esto es equivalente a math.ceil(total_items / items_por_pagina)
