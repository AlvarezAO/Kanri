from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


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
                       description="Numero Telefono Usuario.")
    phone_number_alternative: Optional[str] = Field(None,
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


class UserUpdate(UserCreate):
    password: str = Field(...,
                       example="MiClave1234",
                       description="Contraseña del usuario.",
                       min_length=8,
                       max_length=256
                       )
    web_access: str = Field(None,
                            example="Y",
                            description="Indica si el usuario tiene acceso web. 'Y' para Sí, 'N' para No."
                            )


class UserRead(UserCreate):
    user_id: str = Field(...,
                            example="fj32j-32daa-323dvsds-323dsa",
                            description="Identificador único del usuario registrado"
                            )
    change_password: str = Field(None,
                               example="N",
                               description="Indica si el usuario debe cambiar la contraseña en el próximo ingreso. 'Y' para Sí, 'N' para No."
                               )
    last_access_date: Optional[datetime] = Field(None,
                                               description="Fecha y hora del último ingreso del usuario al sistema."
                                               )
    user_status: int = Field(None,
                                example=1,
                                description="Estado del usuario. Por ejemplo, 1 para 'Habilitado', 2 para 'Deshabilitado'."
                                )
    created_at: datetime = Field(...,
                                description="Fecha y hora de creación del usuario en el sistema."
                                )
    modification_date: Optional[datetime] = Field(None,
                                                   description="Fecha y hora de la última modificación realizada en los datos del usuario."
                                                   )
    failed_login_attempts: int = Field(None,
                                   example=3,
                                   description="Número de intentos fallidos de ingreso al sistema."
                                   )


class UserDB(UserRead):
    password: str = Field(...,
                       example="MiClave1234",
                       description="Contraseña del usuario.",
                       min_length=8,
                       max_length=256
                       )
    web_access: str = Field(None,
                            example="Y",
                            description="Indica si el usuario tiene acceso web. 'Y' para Sí, 'N' para No."
                            )

