from pydantic import BaseModel, Field
#DTO para asegurar validez de datos entre capas
class HttpResponse(BaseModel):
    status_code: int = Field(..., gt=99, lt=600, json_schema_extra={"example": 201, "description": "Código de estado HTTP de la respuesta"})
    content: dict = Field(..., json_schema_extra={"example": {"message": "Compra creada exitosamente", "compra_id": 1}, "description": "Contenido de la respuesta HTTP"})
class ProductoUnitarioDTO(BaseModel):
    id_producto: int = Field(...,gt=0, json_schema_extra={"example": 1, "description": "ID del producto"})
    cantidad: int = Field(..., gt=0, json_schema_extra={"example": 2, "description": "Cantidad del producto a comprar"})    
class CompraRequestDTO(BaseModel):
    id_usuario: int = Field(...,gt=0, json_schema_extra={"example": 1, "description": "ID del usuario que realiza la compra"})
    productos: list[ProductoUnitarioDTO] = Field(..., json_schema_extra={"example": [{"id_producto": 1, "cantidad": 2}, {"id_producto": 2, "cantidad": 1}], "description": "Lista de productos a comprar con sus cantidades"})
class CompraResponseDTO(BaseModel):
    id: int = Field(...,gt=0, json_schema_extra={"example": 1, "description": "ID de la compra"})
    id_usuario: int = Field(...,gt=0, json_schema_extra={"example": 1, "description": "ID del usuario que realiza la compra"})
    productos: list[ProductoUnitarioDTO] = Field(..., json_schema_extra={"example": [{"id_producto": 1, "cantidad": 2}, {"id_producto": 2, "cantidad": 1}], "description": "Lista de productos comprados con sus cantidades"})
    fecha: str = Field(..., json_schema_extra={"example": "2024-04-27T12:34:56", "description": "Fecha y hora de la compra"})
    total: float = Field(..., gt=0, json_schema_extra={"example": 29.99, "description": "Total de la compra"})
    estado: str = Field(..., json_schema_extra={"example": "completada", "description": "Estado de la compra"})
class UsuarioDTO(BaseModel):
    id: int = Field(...,gt=0, json_schema_extra={"example": 1, "description": "ID del usuario"})
    nombre: str = Field(..., json_schema_extra={"example": "Juan Pérez", "description": "Nombre del usuario"})
    email: str = Field(..., json_schema_extra={"example": "juan.perez@example.com", "description": "Correo electrónico del usuario"})
    es_activo: bool = Field(..., json_schema_extra={"example": True, "description": "Indica si el usuario está activo"})
class ProductoDTO(BaseModel):
    id: int = Field(...,gt=0, json_schema_extra={"example": 1, "description": "ID del producto"})
    nombre: str = Field(..., json_schema_extra={"example": "Manzanas", "description": "Nombre del producto"})
    id_gremio: int = Field(...,gt=0, json_schema_extra={"example": 2, "description": "ID del gremio al que pertenece el producto"})
    precio: float = Field(..., gt=0, json_schema_extra={"example": 3.5, "description": "Precio del producto"})
    unidad: str = Field(..., json_schema_extra={"example": "kg", "description": "Unidad de medida del producto"})
    stock: int = Field(..., ge=0, json_schema_extra={"example": 100, "description": "Cantidad disponible en stock del producto"})