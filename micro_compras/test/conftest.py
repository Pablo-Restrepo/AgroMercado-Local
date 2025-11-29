import pytest
from unittest.mock import patch, MagicMock
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from infraestructure.db.modelsSQL import (
    UsuarioModel, ProductoModel, CompraModel, 
    ProductoUnitarioModel, EnvioModel
)
from sqlmodel import SQLModel

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


# Mock global de RabbitMQ para todos los tests
@pytest.fixture(autouse=True)
def mock_rabbitmq():
    """Mock global de RabbitMQ que se aplica a todos los tests."""
    with patch('infraestructure.broker.publisher_rabbitmq._get_connection') as mock_conn:
        mock_channel = MagicMock()
        mock_conn.return_value.channel.return_value = mock_channel
        with patch('infraestructure.broker.publisher_rabbitmq.pika') as mock_pika:
            mock_pika.BlockingConnection.return_value = MagicMock()
            yield mock_conn


@pytest.fixture
def auth_headers_cliente():
    """Headers de autenticación para un cliente."""
    return {"X-Test-Role": "cliente", "X-Test-User-Id": "1"}


@pytest.fixture
def auth_headers_productor():
    """Headers de autenticación para un productor admin."""
    return {"X-Test-Role": "productor-admin", "X-Test-User-Id": "2"}


@pytest.fixture
async def async_client(mock_rabbitmq):
    """Cliente HTTP asíncrono para pruebas con DB en memoria."""
    from fastapi import FastAPI, Request
    from api.compra_controller import router as compra_router
    from api.envio_controller import router as envio_router
    from api.exceptions import register_exception_handlers
    from core.auth_middleware import get_current_user
    from domain.entities.usuario import RolEnum
    from infraestructure.repositories import (
        CompraRepository, UsuarioRepository, 
        ProductoRepository, EnvioRepository
    )
    from application.services import (
        CompraService, UsuarioService, 
        ProductoService, EnvioService
    )
    import deps
    
    # Crear engine DENTRO del fixture async (mismo event loop)
    engine = create_async_engine(
        TEST_DATABASE_URL, 
        echo=False,
        connect_args={"check_same_thread": False}
    )
    
    # Crear tablas
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    # Crear session factory
    session_factory = async_sessionmaker(
        engine, 
        expire_on_commit=False, 
        class_=AsyncSession
    )
    
    # Insertar datos de prueba
    async with session_factory() as session:
        usuario1 = UsuarioModel(
            u_id=1, u_nombre="Cliente Test",
            u_email="cliente@test.com", u_es_activo=True
        )
        usuario2 = UsuarioModel(
            u_id=2, u_nombre="Usuario Inactivo",
            u_email="inactivo@test.com", u_es_activo=False
        )
        producto1 = ProductoModel(
            p_id=1, p_nombre="Manzanas", p_id_gremio=1,
            p_precio=2.50, p_unidad="kg", p_stock=100
        )
        producto2 = ProductoModel(
            p_id=2, p_nombre="Naranjas", p_id_gremio=1,
            p_precio=3.00, p_unidad="kg", p_stock=50
        )
        producto3 = ProductoModel(
            p_id=3, p_nombre="Leche", p_id_gremio=2,
            p_precio=1.50, p_unidad="litro", p_stock=200
        )
        session.add_all([usuario1, usuario2, producto1, producto2, producto3])
        await session.commit()
    
    # Crear app
    app = FastAPI()
    register_exception_handlers(app)
    
    # Mock de autenticación
    def mock_get_current_user(request: Request):
        role = request.headers.get("X-Test-Role", "cliente")
        user_id = int(request.headers.get("X-Test-User-Id", "1"))
        role_map = {
            "cliente": RolEnum.CLIENTE,
            "productor-admin": RolEnum.PRODUCTOR_ADMIN,
            "productor-afiliado": RolEnum.PRODUCTOR_AFILIADO,
        }
        return {
            "id": user_id, "user_id": user_id, "sub": user_id,
            "email": f"user{user_id}@test.com",
            "username": f"user_{user_id}",
            "rol": role_map.get(role, RolEnum.CLIENTE)
        }
    
    # Crear repositorios y servicios
    compra_repo = CompraRepository()
    usuario_repo = UsuarioRepository()
    producto_repo = ProductoRepository()
    envio_repo = EnvioRepository()
    
    compra_service = CompraService(compra_repo, usuario_repo, producto_repo)
    usuario_service = UsuarioService(usuario_repo)
    producto_service = ProductoService(producto_repo)
    envio_service = EnvioService(envio_repo, producto_repo)
    
    # Override de dependencias
    app.dependency_overrides[get_current_user] = mock_get_current_user
    app.dependency_overrides[deps.get_compra_service] = lambda: compra_service
    app.dependency_overrides[deps.get_usuario_service] = lambda: usuario_service
    app.dependency_overrides[deps.get_producto_service] = lambda: producto_service
    app.dependency_overrides[deps.get_envio_service] = lambda: envio_service
    
    # Registrar routers
    app.include_router(compra_router)
    app.include_router(envio_router)
    
    # Parchear engine y session globalmente
    with patch('infraestructure.db.engine.engine', engine):
        with patch('infraestructure.db.engine.async_session', session_factory):
            # Resetear singletons
            deps._singleton_compra_repo = None
            deps._singleton_usuario_repo = None
            deps._singleton_producto_repo = None
            deps._singleton_envio_repo = None
            deps._singleton_compra_service = None
            deps._singleton_usuario_service = None
            deps._singleton_producto_service = None
            deps._singleton_envio_service = None
            
            transport = ASGITransport(app=app)
            async with AsyncClient(transport=transport, base_url="http://test") as client:
                yield client
    
    # Cleanup
    app.dependency_overrides.clear()
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
def seed_data():
    """Datos de prueba ya insertados por async_client."""
    return {
        "usuario_id": 1,
        "usuario_inactivo_id": 2,
        "productos": [1, 2, 3]
    }