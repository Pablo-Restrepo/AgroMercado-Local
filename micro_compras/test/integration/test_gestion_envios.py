"""
Prueba de Integración 3: Gestión del ciclo de vida de envíos.
"""
import pytest


class TestGestionEnvios:
    """
    Pruebas de integración para el ciclo de vida de envíos.
    """
    
    async def _crear_compra_pagada(self, async_client, auth_headers_cliente):
        """Helper para crear una compra pagada."""
        compra_data = {
            "id_usuario": 1,
            "productos": [{"id_producto": 1, "cantidad": 5}]
        }
        
        response_crear = await async_client.post(
            "/api/compras/",
            json=compra_data,
            headers=auth_headers_cliente
        )
        
        if response_crear.status_code != 201:
            return None
            
        data = response_crear.json()
        compra_id = data.get("compra_id") or data.get("content", {}).get("compra_id")
        
        # Confirmar
        await async_client.post(
            f"/api/compras/{compra_id}/confirmar",
            headers=auth_headers_cliente
        )
        
        # Pagar
        await async_client.post(
            f"/api/compras/{compra_id}/pagar?destino=Calle Test 123",
            headers=auth_headers_cliente
        )
        
        return {"compra_id": compra_id, "usuario_id": 1, "gremio_id": 1}

    @pytest.mark.asyncio
    async def test_ciclo_vida_envio_completo(
        self,
        async_client,
        seed_data,
        auth_headers_cliente,
        auth_headers_productor
    ):
        """
        Test del ciclo de vida completo de un envío.
        """
        compra_info = await self._crear_compra_pagada(async_client, auth_headers_cliente)
        assert compra_info is not None, "No se pudo crear la compra"
        
        gremio_id = compra_info["gremio_id"]
        
        # Obtener envíos del gremio
        response_envios = await async_client.get(
            f"/api/envios/gremio/{gremio_id}",
            headers=auth_headers_productor
        )
        
        assert response_envios.status_code == 200
        data = response_envios.json()
        envios = data.get("envios", data if isinstance(data, list) else [])
        assert len(envios) >= 1
        
        envio = envios[0]
        envio_id = envio["id"]
        
        # Verificar estado inicial
        assert envio["estado"] == "PENDIENTE"
        
        # Transición: PENDIENTE -> DESPACHADO
        response_despachar = await async_client.patch(
            f"/api/envios/{envio_id}?status=DESPACHADO",
            headers=auth_headers_productor
        )
        assert response_despachar.status_code == 200
        
        # Transición: DESPACHADO -> EN_RUTA
        response_en_ruta = await async_client.patch(
            f"/api/envios/{envio_id}?status=EN_RUTA",
            headers=auth_headers_productor
        )
        assert response_en_ruta.status_code == 200
        
        # Transición: EN_RUTA -> ENTREGADO
        response_entregado = await async_client.patch(
            f"/api/envios/{envio_id}?status=ENTREGADO",
            headers=auth_headers_productor
        )
        assert response_entregado.status_code == 200

    @pytest.mark.asyncio
    async def test_transicion_invalida_pendiente_a_en_ruta(
        self,
        async_client,
        seed_data,
        auth_headers_cliente,
        auth_headers_productor
    ):
        """
        Test que verifica que no se puede saltar estados.
        """
        compra_info = await self._crear_compra_pagada(async_client, auth_headers_cliente)
        assert compra_info is not None
        
        gremio_id = compra_info["gremio_id"]
        
        response_envios = await async_client.get(
            f"/api/envios/gremio/{gremio_id}",
            headers=auth_headers_productor
        )
        data = response_envios.json()
        envios = data.get("envios", data if isinstance(data, list) else [])
        envio_id = envios[0]["id"]
        
        # Intentar transición inválida: PENDIENTE -> EN_RUTA
        response = await async_client.patch(
            f"/api/envios/{envio_id}?status=EN_RUTA",
            headers=auth_headers_productor
        )
        
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_transicion_invalida_pendiente_a_entregado(
        self,
        async_client,
        seed_data,
        auth_headers_cliente,
        auth_headers_productor
    ):
        """
        Test que verifica que no se puede entregar sin despachar.
        """
        compra_info = await self._crear_compra_pagada(async_client, auth_headers_cliente)
        assert compra_info is not None
        
        gremio_id = compra_info["gremio_id"]
        
        response_envios = await async_client.get(
            f"/api/envios/gremio/{gremio_id}",
            headers=auth_headers_productor
        )
        data = response_envios.json()
        envios = data.get("envios", data if isinstance(data, list) else [])
        envio_id = envios[0]["id"]
        
        # Intentar transición inválida
        response = await async_client.patch(
            f"/api/envios/{envio_id}?status=ENTREGADO",
            headers=auth_headers_productor
        )
        
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_consulta_envios_por_usuario(
        self,
        async_client,
        seed_data,
        auth_headers_cliente
    ):
        """
        Test que verifica la consulta de envíos por usuario.
        """
        compra_info = await self._crear_compra_pagada(async_client, auth_headers_cliente)
        assert compra_info is not None
        
        usuario_id = compra_info["usuario_id"]
        
        response = await async_client.get(
            f"/api/envios/usuario/{usuario_id}",
            headers=auth_headers_cliente
        )
        
        assert response.status_code == 200
        data = response.json()
        envios = data.get("envios", data if isinstance(data, list) else [])
        assert len(envios) >= 1

    @pytest.mark.asyncio
    async def test_usuario_no_puede_ver_envios_de_otro(
        self,
        async_client,
        seed_data,
        auth_headers_cliente
    ):
        """
        Test que verifica control de acceso a envíos.
        """
        response = await async_client.get(
            "/api/envios/usuario/999",
            headers=auth_headers_cliente
        )
        
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_envio_no_existente(
        self,
        async_client,
        seed_data,
        auth_headers_productor
    ):
        """
        Test que verifica manejo de envío inexistente.
        """
        response = await async_client.patch(
            "/api/envios/99999?status=DESPACHADO",
            headers=auth_headers_productor
        )
        
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_consulta_envios_gremio_sin_envios(
        self,
        async_client,
        seed_data,
        auth_headers_productor
    ):
        """
        Test que verifica consulta de gremio sin envíos.
        """
        response = await async_client.get(
            "/api/envios/gremio/999",
            headers=auth_headers_productor
        )
        
        assert response.status_code == 200
        data = response.json()
        envios = data.get("envios", data if isinstance(data, list) else [])
        assert envios == []

    @pytest.mark.asyncio
    async def test_cliente_no_puede_actualizar_envio(
        self,
        async_client,
        seed_data,
        auth_headers_cliente
    ):
        """
        Test que verifica que cliente no puede actualizar estado de envío.
        """
        response = await async_client.patch(
            "/api/envios/1?status=DESPACHADO",
            headers=auth_headers_cliente
        )
        
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_estado_envio_invalido(
        self,
        async_client,
        seed_data,
        auth_headers_cliente,
        auth_headers_productor
    ):
        """
        Test que verifica manejo de estado inválido.
        """
        compra_info = await self._crear_compra_pagada(async_client, auth_headers_cliente)
        assert compra_info is not None
        
        gremio_id = compra_info["gremio_id"]
        
        response_envios = await async_client.get(
            f"/api/envios/gremio/{gremio_id}",
            headers=auth_headers_productor
        )
        data = response_envios.json()
        envios = data.get("envios", data if isinstance(data, list) else [])
        envio_id = envios[0]["id"]
        
        response = await async_client.patch(
            f"/api/envios/{envio_id}?status=ESTADO_INVALIDO",
            headers=auth_headers_productor
        )
        
        assert response.status_code in [400, 422]