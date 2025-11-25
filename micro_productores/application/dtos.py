from pydantic import BaseModel, Field
#DTO para asegurar validez de datos entre capas
class PersonaRegistro(BaseModel):
    p_cedula: str = Field(..., max_length=20,json_schema_extra={"example": "1234567890", "description": "Cédula única de la persona"})
    p_apellido: str = Field(..., max_length=50,json_schema_extra={"example": "Pérez", "description": "Apellido de la persona"})
    p_nombre: str = Field(..., max_length=50,json_schema_extra={"example": "Juan", "description": "Nombre de la persona"})
    p_fecha_nacimiento: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", json_schema_extra={"example": "1990-01-01", "description": "Fecha de nacimiento de la persona"})
    p_direccion: str = Field(..., max_length=100,json_schema_extra={"example": "Av. Siempre Viva 742", "description": "Dirección de la persona"})
    p_telefono: str = Field(..., max_length=15,json_schema_extra={"example": "123456789", "description": "Teléfono de la persona"})
class UsuarioRegistro(BaseModel):
    u_nombre_usuario: str = Field(..., max_length=50,json_schema_extra={"example": "juanperez", "description": "Nombre de usuario del nuevo usuario"})
    u_contrasenia: str = Field(..., min_length=8, max_length=100,json_schema_extra={"example": "contraseniaSegura123", "description": "Contraseña del nuevo usuario"})
    u_email: str = Field(..., max_length=100,json_schema_extra={"example": "juan.perez@example.com", "description": "Email del nuevo usuario"})
    u_rol:str = Field(default="productor-afiliado", max_length=30,json_schema_extra={"example": "productor-afiliado", "description": "Rol del nuevo usuario"})
    persona: PersonaRegistro
    
class RegistrarProductorEnGremioDTO(BaseModel):    
    #El codigo no es obligatorio porque se puede generar automáticamente
    codigo: str | None = Field(None,max_length=10, json_schema_extra={"example": "PROD123", "description": "Código único del productor"})    
    id_gremio: int = Field(..., json_schema_extra={"example": 1, "description": "ID del gremio al que pertenece el productor"})
    #Se asocia el usuario para capturar los datos que posteriormente se van
    #a enviar al micro de usuarios
    usuario: UsuarioRegistro

class CrearGremioDTO(BaseModel):    
    nombre: str = Field(..., min_length=3, max_length=100, json_schema_extra={"example": "Gremio de Agricultores", "description": "Nombre del gremio a crear"})
    descripcion: str = Field(..., min_length=10, max_length=500, json_schema_extra={"example": "Gremio dedicado a la agricultura sostenible", "description": "Descripción del gremio a crear"})
    ubicacion: str = Field(..., min_length=5, max_length=200, json_schema_extra={"example": "Vereda Santa Barbara, Popayán", "description": "Ubicación del gremio a crear"})

class ProductorResponseDTO(BaseModel):
    id: int
    codigo: str | None
    nombres: str
    apellidos: str
    id_gremio: int | None
    rol: str | None
    es_activo: bool
    u_id: int

class GremioResponseDTO(BaseModel):
    id: int
    nombre: str
    descripcion: str
    ubicacion: str
    productores: list[ProductorResponseDTO] = []    

class CrearProductorDTO(BaseModel):
    u_id: int
    nombres: str
    apellidos: str    