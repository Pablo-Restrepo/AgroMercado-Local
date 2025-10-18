from typing import Optional, List
from datetime import date, datetime
from sqlmodel import SQLModel, Field, Relationship

class PersonaModel(SQLModel, table=True):
    __tablename__ = "persona"  # Define explícitamente el nombre de la tabla
    
    p_id: Optional[int] = Field(default=None, primary_key=True)
    p_cedula: str = Field(unique=True, max_length=20)
    p_apellido: str = Field(max_length=100)
    p_nombre: str = Field(max_length=100)
    p_fecha_nacimiento: str = Field(max_length=10)  # O usa date si prefieres
    p_direccion: str = Field(max_length=255)
    p_telefono: str = Field(max_length=15)

    # Relación con usuarios
    usuarios: List["UsuarioModel"] = Relationship(back_populates="persona")


class UsuarioModel(SQLModel, table=True):
    __tablename__ = "usuario"  # Define explícitamente el nombre de la tabla
    
    u_id: Optional[int] = Field(default=None, primary_key=True)
    u_nombre_usuario: str = Field(max_length=100)
    u_contrasenia: str = Field(max_length=255)
    u_email: str = Field(unique=True, max_length=100)
    p_id: Optional[int] = Field(default=None, foreign_key="persona.p_id")

    # Relación con persona
    persona: Optional[PersonaModel] = Relationship(back_populates="usuarios")