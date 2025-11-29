import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

from domain.entities.usuario import Usuario
from domain.entities.producto import Producto
from domain.entities.producto_unitario import ProductoUnitario
from domain.entities.compra import Compra
from domain.entities.envio import Envio
from domain.entities.estado_compra import EstadoCreada, EstadoConfirmada, EstadoPagada
from domain.entities.estado_envio import EstadoPendiente
from application.dtos import CompraRequestDTO, ProductoUnitarioDTO, UsuarioDTO, ProductoDTO


# ========== ENTIDADES DE DOMINIO ==========

@pytest.fixture
def usuario_activo():
    return Usuario(id=1, nombre="Juan Pérez", email="juan@example.com", es_activo=True)


@pytest.fixture
def usuario_inactivo():
    return Usuario(id=2, nombre="María López", email="maria@example.com", es_activo=False)


@pytest.fixture
def producto_con_stock():
    return Producto(id=1, nombre="Manzanas", id_gremio=1, precio=2.50, unidad="kg", stock=100)


@pytest.fixture
def producto_sin_stock():
    return Producto(id=2, nombre="Naranjas", id_gremio=1, precio=3.00, unidad="kg", stock=0)


@pytest.fixture
def producto_unitario():
    return ProductoUnitario(id_producto=1, cantidad=5, precio_unitario=2.50, unidad="kg")


@pytest.fixture
def compra_creada(usuario_activo, producto_unitario):
    return Compra(
        id=1,
        id_usuario=usuario_activo.id,
        productos=[producto_unitario],
        fecha=datetime.now(),
        total=12.50,
        estado=EstadoCreada()
    )


@pytest.fixture
def compra_confirmada(usuario_activo, producto_unitario):
    return Compra(
        id=2,
        id_usuario=usuario_activo.id,
        productos=[producto_unitario],
        fecha=datetime.now(),
        total=12.50,
        estado=EstadoConfirmada()
    )


@pytest.fixture
def compra_pagada(usuario_activo, producto_unitario):
    return Compra(
        id=3,
        id_usuario=usuario_activo.id,
        productos=[producto_unitario],
        fecha=datetime.now(),
        total=12.50,
        estado=EstadoPagada()
    )


@pytest.fixture
def envio_pendiente(compra_pagada):
    return Envio(
        id=1,
        id_gremio=1,
        compra=compra_pagada,
        destino="Calle 123",
        valor=10000.0,
        estado=EstadoPendiente()
    )


# ========== DTOs ==========

@pytest.fixture
def compra_request_dto():
    return CompraRequestDTO(
        id_usuario=1,
        productos=[
            ProductoUnitarioDTO(id_producto=1, cantidad=5),
            ProductoUnitarioDTO(id_producto=2, cantidad=3)
        ]
    )


@pytest.fixture
def usuario_dto():
    return UsuarioDTO(id=1, nombre="Test User", email="test@example.com", es_activo=True)


@pytest.fixture
def producto_dto():
    return ProductoDTO(id=1, nombre="Test Product", id_gremio=1, precio=10.0, unidad="kg", stock=50)


# ========== MOCKS DE REPOSITORIOS ==========

@pytest.fixture
def mock_usuario_repo():
    repo = AsyncMock()
    repo.get_usuario_by_id = AsyncMock()
    repo.get_usuario_by_email = AsyncMock()
    repo.save_usuario = AsyncMock()
    return repo


@pytest.fixture
def mock_producto_repo():
    repo = AsyncMock()
    repo.get_producto_by_id = AsyncMock()
    repo.get_productos = AsyncMock()
    repo.save_producto = AsyncMock()
    return repo


@pytest.fixture
def mock_compra_repo():
    repo = AsyncMock()
    repo.save_compra = AsyncMock()
    repo.get_compra_by_id = AsyncMock()
    repo.get_compras = AsyncMock()
    repo.get_compras_by_usuario = AsyncMock()
    repo.update_compra = AsyncMock()
    return repo


@pytest.fixture
def mock_envio_repo():
    repo = AsyncMock()
    repo.save_envio = AsyncMock()
    repo.get_envio_by_id = AsyncMock()
    repo.update_envio = AsyncMock()
    repo.get_envios_by_id_gremio = AsyncMock()
    repo.get_envios_by_usuario = AsyncMock()
    return repo