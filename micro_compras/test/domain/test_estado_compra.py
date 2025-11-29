import pytest
from unittest.mock import MagicMock
from domain.entities.estado_compra import (
    EstadoCreada, EstadoConfirmada, EstadoPagada,
    EstadoEnviada, EstadoCancelada
)


class TestEstadoCreada:
    def test_confirmar(self):
        estado = EstadoCreada()
        compra = MagicMock()
        
        estado.confirmar(compra)
        
        assert isinstance(compra.estado, EstadoConfirmada)

    def test_pagar_falla(self):
        estado = EstadoCreada()
        compra = MagicMock()
        
        with pytest.raises(Exception, match="No puedes pagar una compra no confirmada"):
            estado.pagar(compra)

    def test_cancelar(self):
        estado = EstadoCreada()
        compra = MagicMock()
        
        estado.cancelar(compra)
        
        assert isinstance(compra.estado, EstadoCancelada)


class TestEstadoConfirmada:
    def test_pagar(self):
        estado = EstadoConfirmada()
        compra = MagicMock()
        
        estado.pagar(compra)
        
        assert isinstance(compra.estado, EstadoPagada)

    def test_confirmar_falla(self):
        estado = EstadoConfirmada()
        compra = MagicMock()
        
        with pytest.raises(Exception, match="La compra ya está confirmada"):
            estado.confirmar(compra)


class TestEstadoPagada:
    def test_enviar(self):
        estado = EstadoPagada()
        compra = MagicMock()
        
        estado.enviar(compra)
        
        assert isinstance(compra.estado, EstadoEnviada)

    def test_cancelar_falla(self):
        estado = EstadoPagada()
        compra = MagicMock()
        
        with pytest.raises(Exception, match="No se puede cancelar una compra pagada"):
            estado.cancelar(compra)