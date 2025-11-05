import pytest
from unittest.mock import AsyncMock, Mock

from application.services import ProductorService
from domain.models import Productor

@pytest.mark.asyncio
async def test_crear_productor_rolls_back_and_elimina_usuario(monkeypatch):
    # Preparar domain Productor que devolverá el mapper
    productor_domain = Productor(
        id=None, codigo=None, nombres="Juan", apellidos="Perez",
        id_gremio=None, rol="NONE", es_activo=True
    )

    # Patch del mapper dentro del módulo services (services importó el mapper al cargar)
    monkeypatch.setattr("application.services.productorDTO_a_productor", lambda dto: productor_domain)

    # Patch de registrar_usuario que simula éxito y devuelve u_id
    monkeypatch.setattr("application.services.registrar_usuario",
                        lambda usuario: {"status": "success", "data": {"u_id": 123}})

    # Spy/mock para eliminar_usuario_por_id para verificar llamada
    eliminar_mock = Mock()
    monkeypatch.setattr("application.services.eliminar_usuario_por_id", eliminar_mock)

    # Repositorio productor: es_codigo_existente -> False, agregar_productor -> lanza excepción
    productor_repo = Mock()
    productor_repo.es_codigo_existente = AsyncMock(return_value=False)
    productor_repo.agregar_productor = AsyncMock(side_effect=Exception("DB failure"))
    productor_repo.obtener_productor_por_id = AsyncMock(return_value=None)
    productor_repo.actualizar_productor = AsyncMock()

    # Gremio repo no usado en este test, puede ser un Mock simple
    gremio_repo = Mock()

    svc = ProductorService(productor_repo, gremio_repo)

    # Llamada que debe lanzar ValueError y provocar la limpieza (eliminar usuario)
    with pytest.raises(ValueError):
        await svc.crear_productor(Mock(usuario=Mock()))  # el DTO real no importa: el mapper está parcheado

    # Verificar que se intentó eliminar el usuario creado con el u_id retornado
    eliminar_mock.assert_called_once_with(123)