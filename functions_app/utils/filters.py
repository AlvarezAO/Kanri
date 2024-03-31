from sqlalchemy import and_, asc, desc
from typing import Optional, Type, List, Any
from sqlalchemy.orm import Query as SQLAlchemyQuery


# Filtros
def apply_filters(query: SQLAlchemyQuery, model: Type[Any], filters_str: Optional[str], allowed_fields: List[str]) -> SQLAlchemyQuery:
    if filters_str:
        filter_clauses = []
        for filter_pair in filters_str.split(','):
            try:
                key, value = filter_pair.split(':', 1)
                if key in allowed_fields:
                    field = getattr(model, key)
                    filter_clauses.append(field.ilike(f"%{value}%"))
            except ValueError:
                continue  # Ignora los pares de filtro mal formados
        query = query.filter(and_(*filter_clauses))
    return query


# Orden
def apply_order(query: SQLAlchemyQuery, model: Type[Any], order_str: Optional[str], allowed_fields: List[str]) -> SQLAlchemyQuery:
    if order_str:
        order_function = desc if order_str.lower() == 'desc' else asc
        order_fields = [order_function(getattr(model, field)) for field in allowed_fields if field in allowed_fields]
        if order_fields:
            query = query.order_by(*order_fields)
    return query
