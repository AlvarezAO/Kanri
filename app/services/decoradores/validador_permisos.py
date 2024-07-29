from fastapi import Request, HTTPException, status
from functools import wraps


def require_permission(permission: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            if not request:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request not found")

            # Extrae el token del encabezado de autorización
            token = request.headers.get("Authorization")
            if not token or not token.startswith("Bearer "):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
            token = token.split(" ")[1]

            # Verifica los permisos del usuario
            # (Implementa tu lógica de verificación de permisos aquí)
            user_permissions = get_user_permissions(token)  # Supón que esta función obtiene permisos del usuario
            if permission not in user_permissions:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
            return await func(*args, **kwargs)
        return wrapper
    return decorator
