import pytest
from unittest.mock import AsyncMock
from application.services import EnvioService
from domain.exceptions import DomainError
from domain.entities.estado_envio import EstadoDespachado, EstadoEnRuta


class TestEnvioService:
    @pytest.fixture
    def envio_service(self, mock_envio_repo, mock_producto_repo):
        return EnvioService(mock_envio_repo, mock_producto_repo)

    @pytest.mark.asyncio
    async def test_generar_envios_exitoso(
        self, envio_service, mock_producto_repo, mock_envio_repo,
        compra_pagada, producto_con_stock
    ):
        mock_producto_repo.get_producto_by_id.return_value = producto_con_stock
        mock_envio_repo.save_envio.return_value = AsyncMock()
        
        await envio_service.generar_envios(compra_pagada, "Calle 123")
        
        mock_envio_repo.save_envio.assert_called()

    @pytest.mark.asyncio
    async def test_generar_envios_producto_no_existe(
        self, envio_service, mock_producto_repo, compra_pagada
    ):
        mock_producto_repo.get_producto_by_id.return_value = None
        
        with pytest.raises(DomainError) as exc_info:
            await envio_service.generar_envios(compra_pagada, "Calle 123")
        
        assert exc_info.value.code == "PRODUCT_NOT_FOUND"

    @pytest.mark.asyncio
    async def test_update_envio_status_despachar(
        self, envio_service, mock_envio_repo, envio_pendiente
    ):
        mock_envio_repo.get_envio_by_id.return_value = envio_pendiente
        mock_envio_repo.update_envio.return_value = envio_pendiente
        
        resultado = await envio_service.update_envio_status(1, "despachado")
        
        assert resultado.status_code == 200

    @pytest.mark.asyncio
    async def test_update_envio_status_en_ruta(
        self, envio_service, mock_envio_repo, envio_pendiente
    ):
        envio_pendiente.despachar_envio()  # Cambiar a despachado primero
        mock_envio_repo.get_envio_by_id.return_value = envio_pendiente
        mock_envio_repo.update_envio.return_value = envio_pendiente
        
        resultado = await envio_service.update_envio_status(1, "en_ruta")
        
        assert resultado.status_code == 200

    @pytest.mark.asyncio
    async def test_update_envio_status_no_existe(self, envio_service, mock_envio_repo):
        mock_envio_repo.get_envio_by_id.return_value = None
        
        with pytest.raises(DomainError) as exc_info:
            await envio_service.update_envio_status(999, "despachado")
        
        assert exc_info.value.code == "ENVIO_NOT_FOUND"

    @pytest.mark.asyncio
    async def test_update_envio_status_invalido(
        self, envio_service, mock_envio_repo, envio_pendiente
    ):
        mock_envio_repo.get_envio_by_id.return_value = envio_pendiente
        
        with pytest.raises(DomainError) as exc_info:
            await envio_service.update_envio_status(1, "estado_invalido")
        
        assert exc_info.value.code == "ENVIO_STATUS_UPDATE_FAILED"


    @pytest.mark.asyncio
    async def test_get_envios_por_gremio(
        self, envio_service, mock_envio_repo, envio_pendiente
    ):
        mock_envio_repo.get_envios_by_id_gremio.return_value = [envio_pendiente]
        
        resultado = await envio_service.get_envios_por_gremio(1)
        
        assert resultado.status_code == 200
        assert "envios" in resultado.content
        assert len(resultado.content["envios"]) == 1

    @pytest.mark.asyncio
    async def test_get_envios_por_usuario(
        self, envio_service, mock_envio_repo, envio_pendiente
    ):
        mock_envio_repo.get_envios_by_usuario.return_value = [envio_pendiente]
        
        resultado = await envio_service.get_envios_por_usuario(1)
        
        assert resultado.status_code == 200
        assert "envios" in resultado.content

