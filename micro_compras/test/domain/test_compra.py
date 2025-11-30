import pytest
from datetime import datetime
from domain.entities.compra import Compra
from domain.entities.producto_unitario import ProductoUnitario
from domain.entities.estado_compra import (
    EstadoCreada, EstadoConfirmada, EstadoPagada, 
    EstadoEnviada, EstadoCancelada, EstadoCompraEnum
)


class TestCompra:
    def test_crear_compra_valida(self, producto_unitario):
        compra = Compra(id_usuario=1, productos=[producto_unitario])
        
        assert compra.id_usuario == 1
        assert len(compra.productos) == 1
        assert isinstance(compra.estado, EstadoCreada)

    def test_crear_compra_sin_usuario_falla(self, producto_unitario):
        with pytest.raises(ValueError, match="Todos los campos son obligatorios"):
            Compra(id_usuario=None, productos=[producto_unitario])

    def test_calcular_total(self):
        productos = [
            ProductoUnitario(id_producto=1, cantidad=2, precio_unitario=10.0, unidad="kg"),
            ProductoUnitario(id_producto=2, cantidad=3, precio_unitario=5.0, unidad="kg")
        ]
        compra = Compra(id_usuario=1, productos=productos)
        
        total = compra.calcular_total()
        
        assert total == 35.0  # (2*10) + (3*5)

    def test_calcular_total_sin_productos(self):
        compra = Compra(id_usuario=1, productos=[])
        
        assert compra.calcular_total() == 0

    def test_confirmar_compra_desde_creada(self, compra_creada):
        compra_creada.confirmar_compra()
        
        assert isinstance(compra_creada.estado, EstadoConfirmada)

    def test_confirmar_compra_vacia_falla(self):
        compra = Compra(id_usuario=1, productos=[])
        
        with pytest.raises(ValueError, match="No se puede confirmar una compra vacía"):
            compra.confirmar_compra()

    def test_pagar_compra_desde_confirmada(self, compra_confirmada):
        compra_confirmada.pagar_compra()
        
        assert isinstance(compra_confirmada.estado, EstadoPagada)

    def test_pagar_compra_desde_creada_falla(self, compra_creada):
        with pytest.raises(Exception, match="No puedes pagar una compra no confirmada"):
            compra_creada.pagar_compra()

    def test_enviar_compra_desde_pagada(self, compra_pagada):
        compra_pagada.enviar_compra()
        
        assert isinstance(compra_pagada.estado, EstadoEnviada)

    def test_cancelar_compra_desde_creada(self, compra_creada):
        compra_creada.cancelar_compra()
        
        assert isinstance(compra_creada.estado, EstadoCancelada)

    def test_to_dict(self, compra_creada):
        resultado = compra_creada.to_dict()
        
        assert "id" in resultado
        assert "id_usuario" in resultado
        assert "productos" in resultado
        assert "estado" in resultado