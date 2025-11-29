import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, MagicMock, AsyncMock
from sqlmodel import SQLModel

# Mockear Eureka y RabbitMQ ANTES de importar la app
@pytest.fixture(scope="session", autouse=True)
def mock_external_services():
    """Mockea servicios externos (Eureka, RabbitMQ) antes de cargar la app."""
    with patch('py_eureka_client.eureka_client.EurekaClient') as mock_eureka:
        mock_eureka_instance = MagicMock()
        mock_eureka_instance.start = AsyncMock()
        mock_eureka_instance.stop = AsyncMock()
        mock_eureka.return_value = mock_eureka_instance
        
        with patch('aio_pika.connect_robust', new_callable=AsyncMock) as mock_rabbit:
            mock_connection = MagicMock()
            mock_channel = MagicMock()
            mock_channel.default_exchange = MagicMock()
            mock_channel.default_exchange.publish = AsyncMock()
            mock_connection.channel = AsyncMock(return_value=mock_channel)
            mock_rabbit.return_value = mock_connection
            
            with patch('infra.publisher_rabbitmq.publish_productor_registration', new_callable=AsyncMock):
                yield


# Importar después de mockear
from main import app
from infra.db.engine import engine, async_session
from infra.db.modelsSQL import ProductorModel, GremioModel
from core.auth_middleware import get_current_user


@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    """Crea las tablas antes de cada test y las limpia después."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture
async def create_productor_admin():
    """Fixture que crea un productor admin directamente en la BD."""
    async with async_session() as session:
        productor = ProductorModel(
            prod_codigo="ADMIN001",
            prod_nombres="Admin",
            prod_apellidos="Test",
            prod_rol="productor-admin",
            prod_es_activo=True,
            u_id=1
        )
        session.add(productor)
        await session.commit()
        await session.refresh(productor)
        return productor  # Retorna el objeto, no una corutina


@pytest.fixture
def mock_auth_admin():
    """Mock de autenticación que retorna un usuario admin."""
    return {
        'user_id': '1',
        'email': 'admin@test.com',
        'username': 'admin_test',
        'rol': 'productor-admin'
    }


@pytest.fixture
def mock_auth_afiliado():
    """Mock de autenticación que retorna un usuario afiliado."""
    return {
        'user_id': '2',
        'email': 'afiliado@test.com',
        'username': 'afiliado_test',
        'rol': 'productor-afiliado'
    }


# =============================================================================
# TEST 1: Integración del flujo completo de creación de gremio
# =============================================================================
@pytest.mark.asyncio
async def test_crear_gremio_integration(create_productor_admin, mock_auth_admin):
    """
    Test de integración: Verifica el flujo completo de creación de un gremio.
    """
    # No usar await aquí, create_productor_admin ya es el objeto
    admin = create_productor_admin
    
    # Sobreescribir la dependencia de autenticación en la app
    app.dependency_overrides[get_current_user] = lambda: mock_auth_admin
    
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                f"/api/gremios/{admin.prod_id}",
                json={
                    "nombre": "Gremio Agricultores",
                    "descripcion": "Gremio dedicado a la producción agrícola sostenible",
                    "ubicacion": "Vereda El Campo, Popayán"
                },
                headers={"Authorization": "Bearer fake_token"}
            )
        
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Gremio Agricultores"
        
        # Verificar persistencia en BD
        async with async_session() as session:
            gremio_db = await session.get(GremioModel, data["id"])
            assert gremio_db is not None
            assert gremio_db.gre_nombre == "Gremio Agricultores"
    finally:
        # Limpiar los overrides después del test
        app.dependency_overrides.clear()


# =============================================================================
# TEST 2: Integración del flujo de agregar productor a gremio
# =============================================================================
@pytest.mark.asyncio
async def test_agregar_productor_a_gremio_integration(mock_auth_admin):
    """
    Test de integración: Verifica el flujo completo de agregar un productor a un gremio.
    """
    async with async_session() as session:
        gremio = GremioModel(
            gre_nombre="Gremio Cafeteros",
            gre_descripcion="Productores de café",
            gre_ubicacion="Eje Cafetero"
        )
        session.add(gremio)
        await session.commit()
        await session.refresh(gremio)
        
        admin = ProductorModel(
            prod_codigo="ADMIN002",
            prod_nombres="Carlos",
            prod_apellidos="Admin",
            prod_rol="productor-admin",
            prod_es_activo=True,
            gre_id=gremio.gre_id,
            u_id=10
        )
        session.add(admin)
        
        nuevo_productor = ProductorModel(
            prod_codigo="PROD001",
            prod_nombres="María",
            prod_apellidos="García",
            prod_rol="NONE",
            prod_es_activo=True,
            gre_id=None,
            u_id=11
        )
        session.add(nuevo_productor)
        await session.commit()
        await session.refresh(nuevo_productor)
        await session.refresh(gremio)
        
        gremio_id = gremio.gre_id
        productor_id = nuevo_productor.prod_id
    
    # Sobreescribir la dependencia de autenticación
    app.dependency_overrides[get_current_user] = lambda: mock_auth_admin
    
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                f"/api/gremios/{gremio_id}/agregar/{productor_id}",
                headers={"Authorization": "Bearer fake_token"}
            )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id_gremio"] == gremio_id
        assert data["rol"] == "productor-afiliado"
    finally:
        app.dependency_overrides.clear()


# =============================================================================
# TEST 3: Integración del flujo de listar productores y permisos
# =============================================================================
@pytest.mark.asyncio
async def test_listar_productores_y_verificar_permisos_integration(mock_auth_afiliado):
    """
    Test de integración: Verifica el flujo de listar productores y validación de permisos.
    """
    async with async_session() as session:
        productores = [
            ProductorModel(
                prod_codigo=f"PROD{i:03d}",
                prod_nombres=f"Productor{i}",
                prod_apellidos=f"Apellido{i}",
                prod_rol="productor-afiliado",
                prod_es_activo=True,
                u_id=100 + i
            )
            for i in range(1, 4)
        ]
        productor_inactivo = ProductorModel(
            prod_codigo="INACTIVO",
            prod_nombres="Inactivo",
            prod_apellidos="Test",
            prod_rol="NONE",
            prod_es_activo=False,
            u_id=999
        )
        productores.append(productor_inactivo)
        
        for p in productores:
            session.add(p)
        await session.commit()
    
    # Sobreescribir la dependencia de autenticación
    app.dependency_overrides[get_current_user] = lambda: mock_auth_afiliado
    
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Listar productores
            response = await client.get(
                "/api/productores/",
                headers={"Authorization": "Bearer fake_token"}
            )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        codigos = [p["codigo"] for p in data]
        assert "INACTIVO" not in codigos
        
        # Verificar que un afiliado NO puede crear gremios
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/gremios/1",
                json={
                    "nombre": "Gremio No Autorizado",
                    "descripcion": "No debería crearse",
                    "ubicacion": "Ninguna"
                },
                headers={"Authorization": "Bearer fake_token"}
            )
        
        assert response.status_code == 403
    finally:
        app.dependency_overrides.clear()