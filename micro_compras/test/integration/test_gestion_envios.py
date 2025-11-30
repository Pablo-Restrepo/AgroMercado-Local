import pytest

class TestGestionEnvios:
    
    # Actualizar nombre del argumento en el helper
    async def _crear_compra_pagada(self, integration_client, auth_headers_cliente):
        compra_data = {
            "id_usuario": 1,
            "productos": [{"id_producto": 1, "cantidad": 5}]
        }
        # Usar integration_client
        res_crear = await integration_client.post("/api/compras/", json=compra_data, headers=auth_headers_cliente)
        if res_crear.status_code != 201:
            pytest.fail(f"Fallo al crear compra: {res_crear.text}")
            
        data = res_crear.json()
        compra_id = data.get("compra_id") or data.get("content", {}).get("compra_id")
        
        res_conf = await integration_client.post(f"/api/compras/{compra_id}/confirmar", headers=auth_headers_cliente)
        if res_conf.status_code != 200:
            pytest.fail(f"Fallo al confirmar: {res_conf.text}")

        res_pagar = await integration_client.post(f"/api/compras/{compra_id}/pagar?destino=Casa", headers=auth_headers_cliente)
        if res_pagar.status_code != 200:
            pytest.fail(f"Fallo al pagar: {res_pagar.text}")
            
        return {"compra_id": compra_id, "usuario_id": 1, "gremio_id": 1}

    def _extraer_envios(self, response_json):
        if isinstance(response_json, list): return response_json
        if "content" in response_json:
            content = response_json["content"]
            if isinstance(content, dict): return content.get("envios", [])
            elif isinstance(content, list): return content
        return response_json.get("envios", [])

    @pytest.mark.asyncio
    async def test_ciclo_vida_envio_completo(self, integration_client, auth_headers_cliente, auth_headers_productor):
        info = await self._crear_compra_pagada(integration_client, auth_headers_cliente)
        
        res = await integration_client.get(f"/api/envios/gremio/{info['gremio_id']}", headers=auth_headers_productor)
        assert res.status_code == 200
        
        envios = self._extraer_envios(res.json())
        assert len(envios) > 0
        envio_id = envios[0]["id"]

        await integration_client.patch(f"/api/envios/{envio_id}?status=DESPACHADO", headers=auth_headers_productor)
        await integration_client.patch(f"/api/envios/{envio_id}?status=EN_RUTA", headers=auth_headers_productor)
        res_final = await integration_client.patch(f"/api/envios/{envio_id}?status=ENTREGADO", headers=auth_headers_productor)
        
        assert res_final.status_code == 200
        
        # Verificación robusta
        res_check = await integration_client.get(f"/api/envios/gremio/{info['gremio_id']}", headers=auth_headers_productor)
        envios_check = self._extraer_envios(res_check.json())
        envio_check = next((e for e in envios_check if e["id"] == envio_id), None)
        assert envio_check["estado"] == "ENTREGADO"

    @pytest.mark.asyncio
    async def test_transicion_invalida_pendiente_a_en_ruta(self, integration_client, auth_headers_cliente, auth_headers_productor):
        info = await self._crear_compra_pagada(integration_client, auth_headers_cliente)
        res = await integration_client.get(f"/api/envios/gremio/{info['gremio_id']}", headers=auth_headers_productor)
        envio_id = self._extraer_envios(res.json())[0]["id"]
        
        res_fail = await integration_client.patch(f"/api/envios/{envio_id}?status=EN_RUTA", headers=auth_headers_productor)
        assert res_fail.status_code == 400

    @pytest.mark.asyncio
    async def test_transicion_invalida_pendiente_a_entregado(self, integration_client, auth_headers_cliente, auth_headers_productor):
        info = await self._crear_compra_pagada(integration_client, auth_headers_cliente)
        res = await integration_client.get(f"/api/envios/gremio/{info['gremio_id']}", headers=auth_headers_productor)
        envio_id = self._extraer_envios(res.json())[0]["id"]
        
        res_fail = await integration_client.patch(f"/api/envios/{envio_id}?status=ENTREGADO", headers=auth_headers_productor)
        assert res_fail.status_code == 400

    @pytest.mark.asyncio
    async def test_consulta_envios_por_usuario(self, integration_client, auth_headers_cliente):
        info = await self._crear_compra_pagada(integration_client, auth_headers_cliente)
        res = await integration_client.get(f"/api/envios/usuario/{info['usuario_id']}", headers=auth_headers_cliente)
        assert res.status_code == 200
        assert len(self._extraer_envios(res.json())) > 0

    @pytest.mark.asyncio
    async def test_usuario_no_puede_ver_envios_de_otro(self, integration_client, auth_headers_cliente):
        res = await integration_client.get("/api/envios/usuario/999", headers=auth_headers_cliente)
        assert res.status_code == 403

    @pytest.mark.asyncio
    async def test_envio_no_existente(self, integration_client, auth_headers_productor):
        res = await integration_client.patch("/api/envios/99999?status=DESPACHADO", headers=auth_headers_productor)
        assert res.status_code == 404

    @pytest.mark.asyncio
    async def test_consulta_envios_gremio_sin_envios(self, integration_client, auth_headers_productor):
        res = await integration_client.get("/api/envios/gremio/999", headers=auth_headers_productor)
        assert res.status_code == 200
        assert len(self._extraer_envios(res.json())) == 0

    @pytest.mark.asyncio
    async def test_cliente_no_puede_actualizar_envio(self, integration_client, auth_headers_cliente):
        res = await integration_client.patch("/api/envios/1?status=DESPACHADO", headers=auth_headers_cliente)
        assert res.status_code == 403

    @pytest.mark.asyncio
    async def test_estado_envio_invalido(self, integration_client, auth_headers_cliente, auth_headers_productor):
        info = await self._crear_compra_pagada(integration_client, auth_headers_cliente)
        res = await integration_client.get(f"/api/envios/gremio/{info['gremio_id']}", headers=auth_headers_productor)
        envio_id = self._extraer_envios(res.json())[0]["id"]
        
        res_fail = await integration_client.patch(f"/api/envios/{envio_id}?status=ESTADO_INVALIDO", headers=auth_headers_productor)
        assert res_fail.status_code in [400, 422]