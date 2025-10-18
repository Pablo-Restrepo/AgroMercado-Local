from typing import Optional, List
from datetime import date, datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String, Date, DateTime, Boolean

class PersonaModel(SQLModel, table=True):
    p_id: Optional[int] = Field(default=None, primary_key=True)
    p_cedula: str = Field(sa_column=Column("p_cedula", String(20), unique=True, nullable=False))
    p_apellido: str = Field(sa_column=Column("p_apellido", String(100), nullable=False))
    p_nombre: str = Field(sa_column=Column("p_nombre", String(100), nullable=False))
    p_fecha_nacimiento: Optional[date] = Field(default=None, sa_column=Column("p_fecha_nacimiento", Date))
    p_direccion: Optional[str] = Field(default=None, sa_column=Column("p_direccion", String(255)))
    p_telefono: Optional[str] = Field(default=None, sa_column=Column("p_telefono", String(15)))

    usuarios: List["UsuarioModel"] = Relationship(back_populates="persona")


class UsuarioModel(SQLModel, table=True):
    u_id: Optional[int] = Field(default=None, primary_key=True)
    u_nombre_usuario: str
    u_contrasenia: str
    u_email: str
    u_fecha_creacion: Optional[datetime] = Field(default=None, sa_column=Column("u_fecha_creacion", DateTime))
    u_es_activo: bool = Field(default=True, sa_column=Column("u_es_activo", Boolean))
    p_id: Optional[int] = Field(default=None, foreign_key="persona.p_id")

    persona: Optional[PersonaModel] = Relationship(back_populates="usuarios")