import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from fastapi import FastAPI

from api.envio_controller import router
from domain.entities.usuario import RolEnum


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


class TestEnvioController:
    def test_get_envios_by_gremio_sin_auth(self, client):
        response = client.get("/api/envios/gremio/1")
        
        assert response.status_code == 403

    def test_update_envio_sin_auth(self, client):
        response = client.patch("/api/envios/1?status=DESPACHADO")
        
        assert response.status_code == 403

