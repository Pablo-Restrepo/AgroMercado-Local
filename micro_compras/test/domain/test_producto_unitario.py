import pytest
from domain.entities.producto_unitario import ProductoUnitario


class TestProductoUnitario:
    def test_crear_producto_unitario_valido(self):
        pu = ProductoUnitario(id_producto=1, cantidad=5, precio_unitario=10.0, unidad="kg")
        
        assert pu.id_producto == 1
        assert pu.cantidad == 5
        assert pu.subtotal == 50.0

    def test_crear_producto_unitario_cantidad_cero_falla(self):
        with pytest.raises(ValueError, match="La cantidad debe ser mayor que cero"):
            ProductoUnitario(id_producto=1, cantidad=0, precio_unitario=10.0, unidad="kg")

    def test_crear_producto_unitario_cantidad_negativa_falla(self):
        with pytest.raises(ValueError, match="La cantidad debe ser mayor que cero"):
            ProductoUnitario(id_producto=1, cantidad=-5, precio_unitario=10.0, unidad="kg")

    def test_calcular_subtotal(self):
        pu = ProductoUnitario(id_producto=1, cantidad=3, precio_unitario=15.0, unidad="kg")
        
        assert pu.calcular_subtotal() == 45.0

    def test_to_dict(self, producto_unitario):
        resultado = producto_unitario.to_dict()
        
        assert "id_producto" in resultado
        assert "cantidad" in resultado
        assert "subtotal" in resultado