from sqlalchemy import Column, String, Integer, DateTime
from functions_app.database.session import Base


class User(Base):
    __tablename__ = "usuarios"

    usuario_id = Column(String(36), primary_key=True)
    nombre = Column(String(100))
    alias = Column(String(100))
    rut = Column(String(16))
    correo = Column(String(100))
    clave = Column(String(256))
    cambiar_clave = Column(String(1))
    ultimo_ingreso = Column(DateTime)
    estado_usuario = Column(Integer, default=1)
    acceso_web = Column(String(1))
    fecha_creacion = Column(DateTime)
    fecha_modificacion = Column(DateTime)
    avatar = Column(String(300))
    ingresos_fallidos = Column(Integer)
    departamento = Column(String(100))
