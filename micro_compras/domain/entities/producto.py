"""Clase Producto que representa un producto en el sistema de micro compras."""
class Producto:
    def __init__(self, id: int, nombre: str, id_gremio: int, precio: float,unidad: str, stock: int):
        if not id_gremio or precio is None or not unidad or stock is None:
            raise ValueError("Todos los campos son obligatorios.")
        self.id = id
        self.nombre = nombre        
        self.id_gremio = id_gremio
        if precio < 0:
            raise ValueError("El precio del producto no puede ser negativo.")        
        self.precio = precio        
        self.unidad = unidad
        if stock < 0:
            raise ValueError("El stock del producto no puede ser negativo.")
        self.stock = stock
    
    def reducir_stock(self, cantidad: int)->bool:
        if self.stock - cantidad < 0:
            return False
        self.stock -= cantidad
        return True