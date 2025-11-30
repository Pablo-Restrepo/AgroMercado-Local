import pytest
from unittest.mock import AsyncMock, MagicMock
from application.handler import handle_create_usuario, handle_create_producto


class TestHandleCreateUsuario:
    @pytest.mark.asyncio
    async def test_handle_create_usuario_exitoso(self, usuario_activo):
        payload = {
            "id": 1,
            "nombre": "Test User",
            "email": "test@example.com",
            "es_activo": True
        }
        message = MagicMock()
        mock_service = AsyncMock()
        mock_service.crear_usuario.return_value = usuario_activo
        
        await handle_create_usuario(payload, message, mock_service)
        
        mock_service.crear_usuario.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_create_usuario_payload_invalido(self):
        payload = {"invalid": "data"}
        message = MagicMock()
        mock_service = AsyncMock()
        
        with pytest.raises(Exception):
            await handle_create_usuario(payload, message, mock_service)


class TestHandleCreateProducto:
    @pytest.mark.asyncio
    async def test_handle_create_producto_exitoso(self, producto_con_stock):
        payload = {
            "id": 1,
            "nombre": "Test Product",
            "id_gremio": 1,
            "precio": 10.0,
            "unidad": "kg",
            "stock": 50
        }
        message = MagicMock()
        mock_service = AsyncMock()
        mock_service.crear_producto.return_value = producto_con_stock
        
        await handle_create_producto(payload, message, mock_service)
        
        mock_service.crear_producto.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_create_producto_payload_invalido(self):
        payload = {"invalid": "data"}
        message = MagicMock()
        mock_service = AsyncMock()
        
        with pytest.raises(Exception):
            await handle_create_producto(payload, message, mock_service)

