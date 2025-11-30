import pytest

class TestValidacionesNegocio:
    
    @pytest.mark.asyncio
    async def test_no_permite_compra_usuario_inexistente(self, integration_client, seed_data, auth_headers_cliente):
        compra_data = { "id_usuario": 9999, "productos": [{"id_producto": 1, "cantidad": 5}] }
        response = await integration_client.post("/api/compras/", json=compra_data, headers=auth_headers_cliente)
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_no_permite_compra_usuario_inactivo(self, integration_client, seed_data, auth_headers_cliente):
        compra_data = { "id_usuario": 2, "productos": [{"id_producto": 1, "cantidad": 5}] }
        response = await integration_client.post("/api/compras/", json=compra_data, headers=auth_headers_cliente)
        assert response.status_code in [403, 404]

    @pytest.mark.asyncio
    async def test_no_permite_compra_producto_inexistente(self, integration_client, seed_data, auth_headers_cliente):
        compra_data = { "id_usuario": 1, "productos": [{"id_producto": 9999, "cantidad": 5}] }
        response = await integration_client.post("/api/compras/", json=compra_data, headers=auth_headers_cliente)
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_no_permite_compra_stock_insuficiente(self, integration_client, seed_data, auth_headers_cliente):
        compra_data = { "id_usuario": 1, "productos": [{"id_producto": 1, "cantidad": 150}] }
        response = await integration_client.post("/api/compras/", json=compra_data, headers=auth_headers_cliente)
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_no_permite_compra_sin_productos(self, integration_client, seed_data, auth_headers_cliente):
        compra_data = { "id_usuario": 1, "productos": [] }
        response = await integration_client.post("/api/compras/", json=compra_data, headers=auth_headers_cliente)
        assert response.status_code in [400, 422]

    @pytest.mark.asyncio
    async def test_control_acceso_productor_no_puede_crear_compra(self, integration_client, seed_data, auth_headers_productor):
        compra_data = { "id_usuario": 1, "productos": [{"id_producto": 1, "cantidad": 5}] }
        response = await integration_client.post("/api/compras/", json=compra_data, headers=auth_headers_productor)
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_control_acceso_cliente_no_puede_ver_envios_gremio(self, integration_client, seed_data, auth_headers_cliente):
        response = await integration_client.get("/api/envios/gremio/1", headers=auth_headers_cliente)
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_reduccion_stock_tras_compra(self, integration_client, seed_data, auth_headers_cliente):
        # Compra 1: 30 unidades
        await integration_client.post("/api/compras/", json={"id_usuario": 1, "productos": [{"id_producto": 1, "cantidad": 30}]}, headers=auth_headers_cliente)
        # Compra 2: 60 unidades
        await integration_client.post("/api/compras/", json={"id_usuario": 1, "productos": [{"id_producto": 1, "cantidad": 60}]}, headers=auth_headers_cliente)
        # Compra 3: 20 unidades (Falla, stock restante 10)
        res = await integration_client.post("/api/compras/", json={"id_usuario": 1, "productos": [{"id_producto": 1, "cantidad": 20}]}, headers=auth_headers_cliente)
        assert res.status_code == 400