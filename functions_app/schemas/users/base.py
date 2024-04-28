from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from sqlalchemy import Enum

from functions_app.src.users.constants import UserStatus
from functions_app.utils.to_camel_models import to_camel


class UserCreate(BaseModel):
    name: str = Field(...,
                        example="Jhon Doe",
                        description="Nombre completo del usuario.",
                        min_length=6,
                        max_length=50
                        )
    alias: str = Field(...,
                       example="Señor Jhon",
                       description="Alias con el que será reconocido el usuario.",
                       min_length=3,
                       max_length=30
                       )
    dni: str = Field(...,
                     example="11111111-1",
                     description="RUT del usuario.",
                     pattern="^\d{7,8}[-][0-9kK]{1}$"
                     )
    email: str = Field(...,
                        example="tu.correo@email.com",
                        pattern="^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$",
                        description="Correo electrónico del usuario.")
    phone_number: str = Field(...,
                       example="999999999",
                       description="Numero Telefono Usuario.",
                       alias="phoneNumber")
    phoneNumberAlternative: Optional[str] = Field(None,
                       example="999999999",
                       description="Numero Alternativo Usuario.")
    avatar: Optional[str] = Field(None,
                                  example="https://miweb.com/miavatar.png",
                                  description="URL del avatar o imagen del usuario."
                                  )
    '''departamento: Optional[str] = Field(...,
                                        example="Tecnología",
                                        description="Departamento o área al que pertenece el usuario.",
                                        min_length=3,
                                        max_length=100
                                        )'''

    class Config:
        from_attributes = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class UserUpdate(UserCreate):
    password: str = Field(...,
                       example="MiClave1234",
                       description="Contraseña del usuario.",
                       min_length=8,
                       max_length=256
                       )
    webAccess: bool = Field(None,
                            example="Y",
                            description="Indica si el usuario tiene acceso web. 'Y' para Sí, 'N' para No."
                            )


class UserRead(UserCreate):
    userId: str = Field(...,
                            example="fj32j-32daa-323dvsds-323dsa",
                            description="Identificador único del usuario registrado"
                            )
    changePassword: bool = Field(None,
                               example="N",
                               description="Indica si el usuario debe cambiar la contraseña en el próximo ingreso. 'Y' para Sí, 'N' para No."
                               )
    lastAccessDate: Optional[datetime] = Field(None,
                                               description="Fecha y hora del último ingreso del usuario al sistema."
                                               )
    userStatus: UserStatus = Field(None,
                                          example=1,
                                          description="Estado del usuario. Por ejemplo, 1 para 'Habilitado', 2 para 'Deshabilitado'."
                                          )
    createdAt: datetime = Field(...,
                                description="Fecha y hora de creación del usuario en el sistema."
                                )
    updatedAt: Optional[datetime] = Field(None,
                                                   description="Fecha y hora de la última modificación realizada en los datos del usuario."
                                                   )
    failedLoginAttempts: int = Field(None,
                                   example=3,
                                   description="Número de intentos fallidos de ingreso al sistema."
                                   )

    class Config:
        from_attributes = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class UserDB(UserRead):
    password: str = Field(...,
                       example="MiClave1234",
                       description="Contraseña del usuario.",
                       min_length=8,
                       max_length=256
                       )
    webAccess: bool = Field(None,
                            example="Y",
                            description="Indica si el usuario tiene acceso web. 'Y' para Sí, 'N' para No."
                            )

