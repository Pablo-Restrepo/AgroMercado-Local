import pytest
from datetime import datetime
from infraestructure.db.mapper import (
    compra_entity_to_model, compra_model_to_entity,
    producto_unitario_entity_to_model, producto_unitario_model_to_entity,
    envio_entity_to_model
)
from infraestructure.db.modelsSQL import CompraModel, ProductoUnitarioModel
from domain.entities.compra import Compra
from domain.entities.producto_unitario import ProductoUnitario
from domain.entities.estado_compra import EstadoCreada, EstadoConfirmada, EstadoCompraEnum


class TestCompraMapper:
    def test_compra_entity_to_model(self, compra_creada):
        model = compra_entity_to_model(compra_creada)
        
        assert model.u_id == compra_creada.id_usuario
        assert model.c_total == compra_creada.total
        assert model.c_estado == EstadoCompraEnum.CREADA

    def test_compra_model_to_entity(self, producto_unitario):
        pu_model = ProductoUnitarioModel(
            pu_id=1,
            p_id=1,
            pu_cantidad=5,
            pu_precio_unitario=2.50,
            pu_unidad="kg",
            pu_subtotal=12.50
        )
        model = CompraModel(
            c_id=1,
            u_id=1,
            c_productos=[pu_model],
            c_fecha=datetime.now(),
            c_total=12.50,
            c_estado=EstadoCompraEnum.CREADA
        )
        
        entity = compra_model_to_entity(model)
        
        assert entity.id == 1
        assert entity.id_usuario == 1
        assert isinstance(entity.estado, EstadoCreada)


class TestProductoUnitarioMapper:
    def test_producto_unitario_entity_to_model(self, producto_unitario):
        model = producto_unitario_entity_to_model(producto_unitario)
        
        assert model.p_id == producto_unitario.id_producto
        assert model.pu_cantidad == producto_unitario.cantidad

    def test_producto_unitario_model_to_entity(self):
        model = ProductoUnitarioModel(
            pu_id=1,
            p_id=1,
            pu_cantidad=5,
            pu_precio_unitario=2.50,
            pu_unidad="kg",
            pu_subtotal=12.50
        )
        
        entity = producto_unitario_model_to_entity(model)
        
        assert entity.id == 1
        assert entity.id_producto == 1
        assert entity.cantidad == 5

