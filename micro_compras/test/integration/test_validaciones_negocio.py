"""
Prueba de Integración 2: Validaciones de reglas de negocio.
"""
import pytest


class TestValidacionesNegocio:
    """
    Pruebas de integración para validar reglas de negocio críticas.
    """
    
    @pytest.mark.asyncio
    async def test_no_permite_compra_usuario_inexistente(
        self,
        async_client,
        seed_data,
        auth_headers_cliente
    ):
        """
        Test que verifica que no se puede crear compra con usuario inexistente.
        """
        compra_data = {
            "id_usuario": 9999,
            "productos": [{"id_producto": 1, "cantidad": 5}]
        }
        
        response = await async_client.post(
            "/api/compras/",
            json=compra_data,
            headers=auth_headers_cliente
        )
        
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_no_permite_compra_usuario_inactivo(
        self,
        async_client,
        seed_data,
        auth_headers_cliente
    ):
        """
        Test que verifica que usuarios inactivos no pueden realizar compras.
        """
        compra_data = {
            "id_usuario": 2,  # Usuario inactivo
            "productos": [{"id_producto": 1, "cantidad": 5}]
        }
        
        response = await async_client.post(
            "/api/compras/",
            json=compra_data,
            headers=auth_headers_cliente
        )
        
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_no_permite_compra_producto_inexistente(
        self,
        async_client,
        seed_data,
        auth_headers_cliente
    ):
        """
        Test que verifica validación de productos existentes.
        """
        compra_data = {
            "id_usuario": 1,
            "productos": [{"id_producto": 9999, "cantidad": 5}]
        }
        
        response = await async_client.post(
            "/api/compras/",
            json=compra_data,
            headers=auth_headers_cliente
        )
        
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_no_permite_compra_stock_insuficiente(
        self,
        async_client,
        seed_data,
        auth_headers_cliente
    ):
        """
        Test que verifica validación de stock disponible.
        """
        compra_data = {
            "id_usuario": 1,
            "productos": [{"id_producto": 1, "cantidad": 150}]  # Stock es 100
        }
        
        response = await async_client.post(
            "/api/compras/",
            json=compra_data,
            headers=auth_headers_cliente
        )
        
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_no_permite_compra_sin_productos(
        self,
        async_client,
        seed_data,
        auth_headers_cliente
    ):
        """
        Test que verifica que no se puede crear compra vacía.
        """
        compra_data = {
            "id_usuario": 1,
            "productos": []
        }
        
        response = await async_client.post(
            "/api/compras/",
            json=compra_data,
            headers=auth_headers_cliente
        )
        
        # Puede ser 400 (validación de negocio) o 422 (validación Pydantic)
        assert response.status_code in [400, 422]

    @pytest.mark.asyncio
    async def test_control_acceso_productor_no_puede_crear_compra(
        self,
        async_client,
        seed_data,
        auth_headers_productor
    ):
        """
        Test que verifica control de acceso por roles.
        """
        compra_data = {
            "id_usuario": 1,
            "productos": [{"id_producto": 1, "cantidad": 5}]
        }
        
        response = await async_client.post(
            "/api/compras/",
            json=compra_data,
            headers=auth_headers_productor
        )
        
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_control_acceso_cliente_no_puede_ver_envios_gremio(
        self,
        async_client,
        seed_data,
        auth_headers_cliente
    ):
        """
        Test que verifica que cliente no puede ver envíos de gremio.
        """
        response = await async_client.get(
            "/api/envios/gremio/1",
            headers=auth_headers_cliente
        )
        
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_reduccion_stock_concurrente(
        self,
        async_client,
        seed_data,
        auth_headers_cliente
    ):
        """
        Test que verifica la reducción de stock tras múltiples compras.
        """
        # Primera compra: 30 unidades
        response1 = await async_client.post(
            "/api/compras/",
            json={"id_usuario": 1, "productos": [{"id_producto": 1, "cantidad": 30}]},
            headers=auth_headers_cliente
        )
        assert response1.status_code == 201, f"Error: {response1.text}"
        
        # Segunda compra: 50 unidades
        response2 = await async_client.post(
            "/api/compras/",
            json={"id_usuario": 1, "productos": [{"id_producto": 1, "cantidad": 50}]},
            headers=auth_headers_cliente
        )
        assert response2.status_code == 201
        
        # Tercera compra: 30 unidades -> debe fallar (stock restante: 20)
        response3 = await async_client.post(
            "/api/compras/",
            json={"id_usuario": 1, "productos": [{"id_producto": 1, "cantidad": 30}]},
            headers=auth_headers_cliente
        )
        
        assert response3.status_code == 400