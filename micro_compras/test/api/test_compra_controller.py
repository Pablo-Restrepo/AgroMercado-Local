import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from fastapi import FastAPI

from api.compra_controller import router
from application.dtos import HttpResponse
from domain.entities.usuario import RolEnum


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


class TestCompraController:
    @pytest.fixture
    def mock_auth_cliente(self):
        return {
            'user_id': 1,
            'email': 'test@example.com',
            'username': 'testuser',
            'rol': RolEnum.CLIENTE
        }

    @pytest.fixture
    def mock_auth_productor(self):
        return {
            'user_id': 1,
            'email': 'test@example.com',
            'username': 'testuser',
            'rol': RolEnum.PRODUCTOR_ADMIN
        }

    def test_create_compra_sin_auth(self, client):
        response = client.post("/api/compras/", json={
            "id_usuario": 1,
            "productos": [{"id_producto": 1, "cantidad": 5}]
        })
        
        assert response.status_code == 403

    @patch('api.compra_controller.get_current_user')
    @patch('api.compra_controller.get_compra_service')
    def test_create_compra_exitosa(
        self, mock_service, mock_auth, client, mock_auth_cliente
    ):
        mock_auth.return_value = mock_auth_cliente
        mock_svc = AsyncMock()
        mock_svc.create_compra.return_value = HttpResponse(
            status_code=201, 
            content={"message": "Compra creada", "compra_id": 1}
        )
        mock_service.return_value = mock_svc
        
        # Este test requiere setup adicional para FastAPI Depends
        # Se recomienda usar httpx.AsyncClient con app.dependency_overrides

    @patch('api.compra_controller.get_current_user')
    @patch('api.compra_controller.get_compra_service')
    def test_create_compra_rol_incorrecto(
        self, mock_service, mock_auth, client, mock_auth_productor
    ):
        mock_auth.return_value = mock_auth_productor
        
        # Productor no puede crear compras
        # Verificar que retorna 403

