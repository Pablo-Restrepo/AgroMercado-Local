from pydantic import BaseModel, Field
#DTO para asegurar validez de datos entre capas
class CrearProductorDTO(BaseModel):
    id: int = Field(..., gt=0, example=1, description="ID único del productor")
    codigo: str = Field(..., min_length=5,max_length=10, example="PROD123", description="Código único del productor")
    nombres: str = Field(..., min_length=3, max_length=50, example="Juan", description="Nombres del productor")
    apellidos: str = Field(..., min_length=2, max_length=50, example="Perez", description="Apellidos del productor")
    id_gremio: int | None = Field(None, example=1, description="ID del gremio al que pertenece el productor")
    rol: str | None = Field(default="NONE", pattern="^(ADMIN|MIEMBRO|NONE)$", example="MIEMBRO", description="Rol del productor en el gremio (si pertenece a uno)")

class CrearGremioDTO(BaseModel):
    id: int = Field(..., gt=0, example=1, description="ID único del gremio a crear")
    nombre: str = Field(..., min_length=3, max_length=100, example="Gremio de Agricultores", description="Nombre del gremio a crear")

class ProductorResponseDTO(BaseModel):
    id: int
    codigo: str
    nombres: str
    apellidos: str
    id_gremio: int | None
    rol: str | None
    es_activo: bool

class GremioResponseDTO(BaseModel):
    id: int
    nombre: str
    productores: list[ProductorResponseDTO] = []    