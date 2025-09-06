from datetime import datetime
from sqlmodel import SQLModel, Field

from uuid import UUID
from datetime import datetime
from sqlmodel import SQLModel, Field
from pydantic import field_validator


class ClienteBase(SQLModel):
    cedula: str = Field(
        min_length=6,
        max_length=15,
        description="Cédula del cliente"
    )
    nombre: str = Field(
        min_length=2,
        max_length=50,
        description="Nombre del cliente"
    )
    apellido: str = Field(
        min_length=2, max_length=50,
        description="Apellido del cliente"
    )
    direccion: str = Field(
        min_length=5, max_length=100,
        description="Dirección del cliente"
    )

    @field_validator("cedula")
    def cedula_must_be_numeric(cls, v):
        if not v.isdigit():
            raise ValueError("La cédula debe contener solo números")
        return v


class ClienteCreate(ClienteBase):
    pass


class ClienteRead(ClienteBase):
    id: UUID
    fecha_creacion: datetime
    fecha_actualizacion: datetime


class ClienteList(SQLModel):
    data: list[ClienteRead]
    count: int


class ClienteUpdate(ClienteBase):
    cedula: str | None
    nombre: str | None
    apellido: str | None
    direccion: str | None
