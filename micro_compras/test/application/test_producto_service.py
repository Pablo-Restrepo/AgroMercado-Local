import pytest
from application.services import ProductoService
from application.dtos import ProductoDTO


class TestProductoService:
    @pytest.fixture
    def producto_service(self, mock_producto_repo):
        return ProductoService(mock_producto_repo)

    @pytest.mark.asyncio
    async def test_crear_producto_exitoso(
        self, producto_service, mock_producto_repo, producto_dto, producto_con_stock
    ):
        mock_producto_repo.save_producto.return_value = producto_con_stock
        
        resultado = await producto_service.crear_producto(producto_dto)
        
        assert resultado.id == producto_con_stock.id
        mock_producto_repo.save_producto.assert_called_once()

