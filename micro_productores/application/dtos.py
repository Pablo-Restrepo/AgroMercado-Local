from pydantic import BaseModel, Field
#DTO para asegurar validez de datos entre capas
class PersonaRegistro(BaseModel):
    p_cedula: str
    p_apellido: str
    p_nombre: str
    p_fecha_nacimiento: str
    p_direccion: str
    p_telefono: str
class UsuarioRegistro(BaseModel):
    u_nombre_usuario: str
    u_contrasenia: str
    u_email: str
    persona: PersonaRegistro
    
class CrearProductorDTO(BaseModel):    
    #El codigo no es obligatorio porque se puede generar automáticamente
    codigo: str | None = Field(None,max_length=10, example="PROD123", description="Código único del productor")
    nombres: str = Field(..., min_length=3, max_length=50, example="Juan", description="Nombres del productor")
    apellidos: str = Field(..., min_length=2, max_length=50, example="Perez", description="Apellidos del productor")
    id_gremio: int | None = Field(None, example=1, description="ID del gremio al que pertenece el productor")
    rol: str | None = Field(default="NONE", pattern="^(ADMIN|MIEMBRO|NONE)$", example="MIEMBRO", description="Rol del productor en el gremio (si pertenece a uno)")
    #Se asocia el usuario para capturar los datos que posteriormente se van
    #a enviar al micro de usuarios
    usuario: UsuarioRegistro

class CrearGremioDTO(BaseModel):    
    nombre: str = Field(..., min_length=3, max_length=100, example="Gremio de Agricultores", description="Nombre del gremio a crear")

class ProductorResponseDTO(BaseModel):
    id: int
    codigo: str | None
    nombres: str
    apellidos: str
    id_gremio: int | None
    rol: str | None
    es_activo: bool
    u_id: int | None

class GremioResponseDTO(BaseModel):
    id: int
    nombre: str
    productores: list[ProductorResponseDTO] = []    

