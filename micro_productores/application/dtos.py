from pydantic import BaseModel, Field
#DTO para asegurar validez de datos entre capas
class CrearProductorDTO(BaseModel):
    id: int = Field(..., gt=0, example=1)
    codigo: str = Field(..., min_length=5,max_length=10, example="PROD123")
    nombres: str = Field(..., min_length=3, max_length=50, example="Juan")
    apellidos: str = Field(..., min_length=2, max_length=50, example="Perez")
    id_gremio: int | None = Field(None, example=1)
    rol: str | None = Field(default="NONE", pattern="^(ADMIN|MIEMBRO|NONE)$", example="MIEMBRO")
    
class CrearGremioDTO(BaseModel):
    id: int = Field(..., gt=0, example=1)
    nombre: str = Field(..., min_length=3, max_length=100, example="Gremio de Agricultores")

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