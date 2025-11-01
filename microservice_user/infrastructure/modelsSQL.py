from sqlmodel import SQLModel, Field, Relationship
from microservice_user.domain.usuario import RolEnum


class PersonaModel(SQLModel, table=True):
    __tablename__ = "persona"  # Define explícitamente el nombre de la tabla

    p_id: int | None = Field(default=None, primary_key=True)
    p_cedula: str = Field(unique=True, max_length=20)
    p_apellido: str = Field(max_length=100)
    p_nombre: str = Field(max_length=100)
    p_fecha_nacimiento: str = Field(max_length=10)  # O usa date si prefieres
    p_direccion: str = Field(max_length=255)
    p_telefono: str = Field(max_length=15)

    # Relación con usuarios
    usuarios: list["UsuarioModel"] = Relationship(back_populates="persona")


class UsuarioModel(SQLModel, table=True):
    __tablename__ = "usuario"  # Define explícitamente el nombre de la tabla
    u_id: int | None = Field(default=None, primary_key=True)
    u_nombre_usuario: str = Field(max_length=100)
    u_contrasenia: str = Field(max_length=255)
    u_email: str = Field(unique=True, max_length=100)
    u_rol: RolEnum = Field(default=RolEnum.CLIENTE, max_length=50)
    p_id: int | None = Field(default=None, foreign_key="persona.p_id")

    # Relación con persona
    persona: PersonaModel | None = Relationship(back_populates="usuarios")
