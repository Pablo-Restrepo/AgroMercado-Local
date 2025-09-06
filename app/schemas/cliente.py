from uuid import UUID
from datetime import datetime
from sqlmodel import SQLModel, Field


class ClienteBase(SQLModel):
    cedula: str = Field(min_length=1)
    nombre: str = Field(min_length=1)
    apellido: str = Field(min_length=1)
    direccion: str = Field(min_length=1)


class ClienteCreate(ClienteBase):
    pass


class ClienteRead(ClienteBase):
    id: UUID
    fecha_creacion: datetime
    fecha_actualizacion: datetime


class ClienteList(SQLModel):
    data: list[ClienteRead]
    count: int


class ClienteUpdate(SQLModel):
    cedula: str | None = Field(default=None, min_length=1)
    nombre: str | None = Field(default=None, min_length=1)
    apellido: str | None = Field(default=None, min_length=1)
    direccion: str | None = Field(default=None, min_length=1)
