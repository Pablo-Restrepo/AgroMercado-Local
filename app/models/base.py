from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import Field
from sqlmodel import SQLModel as _SQLModel

# Migrar a infraestructura
class SQLModel(_SQLModel):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        description='Unique ID',
    )
    fecha_creacion: datetime = Field(
        default_factory=datetime.now, description='Fecha de creacion')
    fecha_actualizacion: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={'onupdate': datetime.now},
        description='Fecha de actualizacion',
    )
