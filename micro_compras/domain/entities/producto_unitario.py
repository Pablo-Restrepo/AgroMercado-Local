"""Clase que representa la compra unitaria de un producto."""
class ProductoUnitario:
    def __init__(self,id_producto: int, cantidad: int,id:int=None, precio_unitario: float = None, unidad: str = None):
        if id_producto is None or cantidad is None:
            raise ValueError("Todos los campos son obligatorios.")
        self.id = id        
        self.id_producto = id_producto
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.unidad = unidad
        self.subtotal = self.calcular_subtotal()
    def calcular_subtotal(self)->float:
        self.subtotal = self.cantidad * self.precio_unitario
        return self.subtotal
    def to_dict(self)-> dict:
        return {
            "id": self.id,
            "id_producto": self.id_producto,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "unidad": self.unidad,
            "subtotal": self.subtotal
        }