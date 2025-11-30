import pytest
from unittest.mock import AsyncMock, patch
from application.services import CompraService
from application.dtos import CompraRequestDTO, ProductoUnitarioDTO
from domain.exceptions import DomainError
from domain.entities.estado_compra import EstadoCreada, EstadoConfirmada


class TestCompraService:
    @pytest.fixture
    def compra_service(self, mock_compra_repo, mock_usuario_repo, mock_producto_repo):
        return CompraService(mock_compra_repo, mock_usuario_repo, mock_producto_repo)

    @pytest.mark.asyncio
    async def test_create_compra_exitosa(
        self, compra_service, mock_usuario_repo, mock_producto_repo, 
        mock_compra_repo, usuario_activo, producto_con_stock
    ):
        # Arrange
        mock_usuario_repo.get_usuario_by_id.return_value = usuario_activo
        mock_producto_repo.get_producto_by_id.return_value = producto_con_stock
        mock_compra_repo.save_compra.return_value = AsyncMock(id=1)
        
        dto = CompraRequestDTO(
            id_usuario=1,
            productos=[ProductoUnitarioDTO(id_producto=1, cantidad=5)]
        )
        
        # Act
        with patch('application.services.publish_stock_updates'):
            resultado = await compra_service.create_compra(dto)
        
        # Assert
        assert resultado.status_code == 201
        assert "compra_id" in resultado.content

    @pytest.mark.asyncio
    async def test_create_compra_usuario_no_existe(
        self, compra_service, mock_usuario_repo
    ):
        mock_usuario_repo.get_usuario_by_id.return_value = None
        dto = CompraRequestDTO(
            id_usuario=999,
            productos=[ProductoUnitarioDTO(id_producto=1, cantidad=5)]
        )
        
        with pytest.raises(DomainError) as exc_info:
            await compra_service.create_compra(dto)
        
        assert exc_info.value.code == "USER_NOT_FOUND"
        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_create_compra_usuario_inactivo(
        self, compra_service, mock_usuario_repo, usuario_inactivo
    ):
        mock_usuario_repo.get_usuario_by_id.return_value = usuario_inactivo
        dto = CompraRequestDTO(
            id_usuario=2,
            productos=[ProductoUnitarioDTO(id_producto=1, cantidad=5)]
        )
        
        with pytest.raises(DomainError) as exc_info:
            await compra_service.create_compra(dto)
        
        assert exc_info.value.code == "USER_NOT_ACTIVE"
        assert exc_info.value.status_code == 403

    @pytest.mark.asyncio
    async def test_create_compra_producto_no_existe(
        self, compra_service, mock_usuario_repo, mock_producto_repo, usuario_activo
    ):
        mock_usuario_repo.get_usuario_by_id.return_value = usuario_activo
        mock_producto_repo.get_producto_by_id.return_value = None
        dto = CompraRequestDTO(
            id_usuario=1,
            productos=[ProductoUnitarioDTO(id_producto=999, cantidad=5)]
        )
        
        with pytest.raises(DomainError) as exc_info:
            await compra_service.create_compra(dto)
        
        assert exc_info.value.code == "PRODUCT_NOT_FOUND"

    @pytest.mark.asyncio
    async def test_create_compra_stock_insuficiente(
        self, compra_service, mock_usuario_repo, mock_producto_repo, 
        usuario_activo, producto_sin_stock
    ):
        mock_usuario_repo.get_usuario_by_id.return_value = usuario_activo
        mock_producto_repo.get_producto_by_id.return_value = producto_sin_stock
        dto = CompraRequestDTO(
            id_usuario=1,
            productos=[ProductoUnitarioDTO(id_producto=2, cantidad=5)]
        )
        
        with pytest.raises(DomainError) as exc_info:
            await compra_service.create_compra(dto)
        
        assert exc_info.value.code == "INSUFFICIENT_STOCK"

    @pytest.mark.asyncio
    async def test_create_compra_sin_productos(
        self, compra_service, mock_usuario_repo, usuario_activo
    ):
        mock_usuario_repo.get_usuario_by_id.return_value = usuario_activo
        dto = CompraRequestDTO(id_usuario=1, productos=[])
        
        with pytest.raises(DomainError) as exc_info:
            await compra_service.create_compra(dto)
        
        assert exc_info.value.code == "EMPTY_PRODUCTS"

    @pytest.mark.asyncio
    async def test_confirmar_compra_exitosa(
        self, compra_service, mock_compra_repo, compra_creada
    ):
        mock_compra_repo.get_compra_by_id.return_value = compra_creada
        mock_compra_repo.update_compra.return_value = None
        
        resultado = await compra_service.confirmar_compra(1)
        
        assert resultado.status_code == 200
        mock_compra_repo.update_compra.assert_called_once()

    @pytest.mark.asyncio
    async def test_confirmar_compra_no_existe(self, compra_service, mock_compra_repo):
        mock_compra_repo.get_compra_by_id.return_value = None
        
        with pytest.raises(DomainError) as exc_info:
            await compra_service.confirmar_compra(999)
        
        assert exc_info.value.code == "COMPRA_NOT_FOUND"

    @pytest.mark.asyncio
    async def test_get_compra_exitosa(self, compra_service, mock_compra_repo, compra_creada):
        mock_compra_repo.get_compra_by_id.return_value = compra_creada
        
        resultado = await compra_service.get_compra(1)
        
        assert resultado.status_code == 200
        assert "id" in resultado.content

    @pytest.mark.asyncio
    async def test_get_compra_no_existe(self, compra_service, mock_compra_repo):
        mock_compra_repo.get_compra_by_id.return_value = None
        
        with pytest.raises(DomainError) as exc_info:
            await compra_service.get_compra(999)
        
        assert exc_info.value.code == "COMPRA_NOT_FOUND"

    @pytest.mark.asyncio
    async def test_get_compras_by_usuario(
        self, compra_service, mock_compra_repo, mock_usuario_repo, 
        usuario_activo, compra_creada
    ):
        mock_usuario_repo.get_usuario_by_id.return_value = usuario_activo
        mock_compra_repo.get_compras_by_usuario.return_value = [compra_creada]
        
        resultado = await compra_service.get_compras_by_usuario(1)
        
        assert resultado.status_code == 200
        assert "compras" in resultado.content
        assert len(resultado.content["compras"]) == 1