import pytest
from domain.entities.envio import Envio
from domain.entities.estado_envio import (
    EstadoPendiente, EstadoDespachado, 
    EstadoEnRuta, EstadoEntregado
)


class TestEnvio:
    def test_crear_envio_valido(self, compra_pagada):
        envio = Envio(id_gremio=1, compra=compra_pagada, destino="Calle 123")
        
        assert envio.id_gremio == 1
        assert envio.destino == "Calle 123"
        assert isinstance(envio.estado, EstadoPendiente)

    def test_despachar_envio_desde_pendiente(self, envio_pendiente):
        envio_pendiente.despachar_envio()
        
        assert isinstance(envio_pendiente.estado, EstadoDespachado)
        assert envio_pendiente.fecha_envio is not None

    def test_enviar_en_ruta_desde_despachado(self, compra_pagada):
        envio = Envio(id_gremio=1, compra=compra_pagada, destino="Calle 123")
        envio.despachar_envio()
        
        envio.enviar_en_ruta()
        
        assert isinstance(envio.estado, EstadoEnRuta)

    def test_entregar_envio_desde_en_ruta(self, compra_pagada):
        envio = Envio(id_gremio=1, compra=compra_pagada, destino="Calle 123")
        envio.despachar_envio()
        envio.enviar_en_ruta()
        
        envio.entregar_envio()
        
        assert isinstance(envio.estado, EstadoEntregado)

    def test_en_ruta_desde_pendiente_falla(self, envio_pendiente):
        with pytest.raises(Exception, match="El envío aún no ha sido despachado"):
            envio_pendiente.enviar_en_ruta()

    def test_to_dict(self, envio_pendiente):
        resultado = envio_pendiente.to_dict()
        
        assert "id_gremio" in resultado
        assert "destino" in resultado
        assert "estado" in resultado