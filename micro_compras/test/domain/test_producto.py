import pytest
from domain.entities.producto import Producto


class TestProducto:
    def test_crear_producto_valido(self):
        producto = Producto(id=1, nombre="Manzanas", id_gremio=1, precio=2.50, unidad="kg", stock=100)
        
        assert producto.id == 1
        assert producto.nombre == "Manzanas"
        assert producto.precio == 2.50
        assert producto.stock == 100

    def test_crear_producto_precio_negativo_falla(self):
        with pytest.raises(ValueError, match="El precio del producto no puede ser negativo"):
            Producto(id=1, nombre="Test", id_gremio=1, precio=-10, unidad="kg", stock=100)

    def test_crear_producto_stock_negativo_falla(self):
        with pytest.raises(ValueError, match="El stock del producto no puede ser negativo"):
            Producto(id=1, nombre="Test", id_gremio=1, precio=10, unidad="kg", stock=-5)

    def test_reducir_stock_exitoso(self, producto_con_stock):
        resultado = producto_con_stock.reducir_stock(50)
        
        assert resultado is True
        assert producto_con_stock.stock == 50

    def test_reducir_stock_insuficiente(self, producto_con_stock):
        resultado = producto_con_stock.reducir_stock(150)
        
        assert resultado is False
        assert producto_con_stock.stock == 100  # No cambió