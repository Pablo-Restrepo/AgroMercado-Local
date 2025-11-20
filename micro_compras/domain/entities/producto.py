class Producto:
    def __init__(self, id: int, nombre: str, nombre_gremio: str, precio: float,unidad: str, stock: int):
        if not id:
            raise ValueError("El ID del producto no puede estar vacío.")
        self.id = id
        self.nombre = nombre
        if not nombre_gremio:
            raise ValueError("El producto debe pertenecer a un gremio.")
        self.nombre_gremio = nombre_gremio
        if precio < 0:
            raise ValueError("El precio del producto no puede ser negativo.")        
        self.precio = precio
        if not unidad:
            raise ValueError("La unidad del producto no puede estar vacía.")
        self.unidad = unidad
        if stock < 0:
            raise ValueError("El stock del producto no puede ser negativo.")
        self.stock = stock
    
    def reducir_stock(self, cantidad: int):
        if self.stock - cantidad < 0:
            raise ValueError("El stock no puede ser negativo después de la actualización.")
        self.stock -= cantidad