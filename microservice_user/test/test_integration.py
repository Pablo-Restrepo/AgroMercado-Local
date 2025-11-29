import sys
from unittest.mock import MagicMock

# Mock del módulo de configuración ANTES de importar cualquier cosa
sys.modules['infrastructure.db_config'] = MagicMock()
sys.modules['infrastructure.db_config'].db_config = {
    "user": "test",
    "password": "test", 
    "host": "localhost",
    "database": "test"
}

import pytest
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool

# Crear engine de prueba antes de importar la app
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Reemplazar el engine antes de importar la app
import infrastructure.engine as eng_module
eng_module.engine = test_engine

from fastapi.testclient import TestClient
from api.main import app
from infrastructure.modelsSQL import PersonaModel, UsuarioModel


@pytest.fixture(name="session", scope="function")
def session_fixture():
    """Crea las tablas y proporciona una sesión limpia para cada test."""
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture(name="client", scope="function")
def client_fixture(session):
    """Cliente de pruebas con base de datos en memoria."""
    return TestClient(app)


@pytest.fixture
def usuario_data():
    """Datos de usuario para registro."""
    return {
        "u_nombre_usuario": "testuser",
        "u_contrasenia": "password123",
        "u_email": "test@example.com",
        "u_rol": "cliente",
        "persona": {
            "p_cedula": "1234567890",
            "p_apellido": "García",
            "p_nombre": "Juan",
            "p_fecha_nacimiento": "1990-01-15",
            "p_direccion": "Calle 123",
            "p_telefono": "3001234567"
        }
    }


class TestRegistroLoginIntegration:
    """Test de integración: Registro completo y login de usuario."""

    def test_registro_y_login_exitoso(self, client, usuario_data):
        # 1. Registrar usuario
        response = client.post("/api/usuarios/registro", json=usuario_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["email"] == usuario_data["u_email"]

        # 2. Login con las credenciales registradas
        login_data = {
            "u_email": usuario_data["u_email"],
            "u_contrasenia": usuario_data["u_contrasenia"]
        }
        response = client.post("/api/usuarios/login", json=login_data)
        assert response.status_code == 200
        login_response = response.json()
        
        assert login_response["u_email"] == usuario_data["u_email"]
        assert login_response["u_nombre_usuario"] == usuario_data["u_nombre_usuario"]
        assert "access_token" in login_response
        assert "refresh_token" in login_response
        assert login_response["token_type"] == "bearer"

    def test_registro_email_duplicado_falla(self, client, usuario_data):
        # 1. Registrar usuario primera vez
        response = client.post("/api/usuarios/registro", json=usuario_data)
        assert response.status_code == 200

        # 2. Intentar registrar con mismo email
        response = client.post("/api/usuarios/registro", json=usuario_data)
        assert response.status_code == 400
        assert "email ya está registrado" in response.json()["detail"].lower()


class TestTokenRefreshIntegration:
    """Test de integración: Flujo completo de refresh token."""

    def test_refresh_token_genera_nuevo_access_token(self, client, usuario_data):
        # 1. Registrar usuario
        client.post("/api/usuarios/registro", json=usuario_data)

        # 2. Login para obtener tokens
        login_data = {
            "u_email": usuario_data["u_email"],
            "u_contrasenia": usuario_data["u_contrasenia"]
        }
        login_response = client.post("/api/usuarios/login", json=login_data)
        tokens = login_response.json()
        original_access = tokens["access_token"]
        refresh = tokens["refresh_token"]

        # 3. Usar refresh token para obtener nuevo access token
        refresh_response = client.post(
            "/api/usuarios/refresh",
            json={"refresh_token": refresh}
        )
        assert refresh_response.status_code == 200
        new_tokens = refresh_response.json()
        
        assert "access_token" in new_tokens
        assert new_tokens["token_type"] == "bearer"
        assert new_tokens["access_token"] != original_access

    def test_refresh_con_token_invalido_falla(self, client):
        response = client.post(
            "/api/usuarios/refresh",
            json={"refresh_token": "token-invalido-123"}
        )
        assert response.status_code == 401


class TestUsuarioMeIntegration:
    """Test de integración: Obtener datos del usuario autenticado."""

    def test_obtener_usuario_autenticado(self, client, usuario_data):
        # 1. Registrar usuario
        client.post("/api/usuarios/registro", json=usuario_data)

        # 2. Login
        login_data = {
            "u_email": usuario_data["u_email"],
            "u_contrasenia": usuario_data["u_contrasenia"]
        }
        login_response = client.post("/api/usuarios/login", json=login_data)
        access_token = login_response.json()["access_token"]

        # 3. Obtener datos del usuario autenticado
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/api/usuarios/me", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["email"] == usuario_data["u_email"]
        assert data["data"]["nombres"] == usuario_data["persona"]["p_nombre"]
        assert data["data"]["apellidos"] == usuario_data["persona"]["p_apellido"]

    def test_acceso_sin_token_falla(self, client):
        response = client.get("/api/usuarios/me")
        assert response.status_code == 403

    def test_acceso_con_token_invalido_falla(self, client):
        headers = {"Authorization": "Bearer token-invalido"}
        response = client.get("/api/usuarios/me", headers=headers)
        assert response.status_code == 401