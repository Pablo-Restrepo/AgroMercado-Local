import pytest
from pydantic import ValidationError
from application.dtos import (
    CompraRequestDTO, ProductoUnitarioDTO, 
    UsuarioDTO, ProductoDTO, HttpResponse
)


class TestProductoUnitarioDTO:
    def test_dto_valido(self):
        dto = ProductoUnitarioDTO(id_producto=1, cantidad=5)
        assert dto.id_producto == 1
        assert dto.cantidad == 5

    def test_id_producto_invalido(self):
        with pytest.raises(ValidationError):
            ProductoUnitarioDTO(id_producto=0, cantidad=5)

    def test_cantidad_invalida(self):
        with pytest.raises(ValidationError):
            ProductoUnitarioDTO(id_producto=1, cantidad=0)


class TestCompraRequestDTO:
    def test_dto_valido(self):
        dto = CompraRequestDTO(
            id_usuario=1,
            productos=[ProductoUnitarioDTO(id_producto=1, cantidad=5)]
        )
        assert dto.id_usuario == 1
        assert len(dto.productos) == 1

    def test_id_usuario_invalido(self):
        with pytest.raises(ValidationError):
            CompraRequestDTO(id_usuario=0, productos=[])


class TestUsuarioDTO:
    def test_dto_valido(self):
        dto = UsuarioDTO(id=1, nombre="Test", email="test@example.com", es_activo=True)
        assert dto.id == 1
        assert dto.nombre == "Test"

    def test_id_invalido(self):
        with pytest.raises(ValidationError):
            UsuarioDTO(id=0, nombre="Test", email="test@example.com", es_activo=True)


class TestProductoDTO:
    def test_dto_valido(self):
        dto = ProductoDTO(id=1, nombre="Test", id_gremio=1, precio=10.0, unidad="kg", stock=50)
        assert dto.id == 1
        assert dto.precio == 10.0

    def test_precio_negativo(self):
        with pytest.raises(ValidationError):
            ProductoDTO(id=1, nombre="Test", id_gremio=1, precio=-10.0, unidad="kg", stock=50)

    def test_stock_negativo(self):
        with pytest.raises(ValidationError):
            ProductoDTO(id=1, nombre="Test", id_gremio=1, precio=10.0, unidad="kg", stock=-5)


class TestHttpResponse:
    def test_response_valido(self):
        response = HttpResponse(status_code=200, content={"message": "OK"})
        assert response.status_code == 200

    def test_status_code_invalido(self):
        with pytest.raises(ValidationError):
            HttpResponse(status_code=50, content={})

