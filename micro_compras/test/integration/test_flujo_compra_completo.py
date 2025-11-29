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


@pytest.fixture(scope="function")
async def test_engine():
    """Crea un engine de prueba con SQLite en memoria."""
    engine = create_async_engine(
        TEST_DATABASE_URL, 
        echo=False,
        connect_args={"check_same_thread": False}
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture(scope="function")
def test_session_factory(test_engine):
    """Crea una factory de sesiones de prueba (sync fixture)."""
    return async_sessionmaker(
        test_engine, 
        expire_on_commit=False, 
        class_=AsyncSession
    )


@pytest.fixture
def auth_headers_cliente():
    """Headers de autenticación para un cliente."""
    return {"X-Test-Role": "cliente", "X-Test-User-Id": "1"}


@pytest.fixture
def auth_headers_productor():
    """Headers de autenticación para un productor admin."""
    return {"X-Test-Role": "productor-admin", "X-Test-User-Id": "2"}


@pytest.fixture
def app_with_test_db(test_engine, test_session_factory):
    """Configura la aplicación con la base de datos de prueba."""
    from fastapi import FastAPI, Request
    from api.compra_controller import router as compra_router
    from api.envio_controller import router as envio_router
    from api.exceptions import register_exception_handlers
    from core.auth_middleware import get_current_user
    from domain.entities.usuario import RolEnum
    
    # Importar repositorios y servicios
    from infraestructure.repositories import (
        CompraRepository, UsuarioRepository, 
        ProductoRepository, EnvioRepository
    )
    from application.services import (
        CompraService, UsuarioService, 
        ProductoService, EnvioService
    )
    
    app = FastAPI()
    register_exception_handlers(app)
    
    # Override de la dependencia get_current_user
    def mock_get_current_user(request: Request):
        role = request.headers.get("X-Test-Role", "cliente")
        user_id = int(request.headers.get("X-Test-User-Id", "1"))
        
        role_map = {
            "cliente": RolEnum.CLIENTE,
            "productor-admin": RolEnum.PRODUCTOR_ADMIN,
            "productor-afiliado": RolEnum.PRODUCTOR_AFILIADO,
        }
        
        return {
            "id": user_id,
            "user_id": user_id,
            "sub": user_id,
            "email": f"user{user_id}@test.com",
            "username": f"user_{user_id}",
            "rol": role_map.get(role, RolEnum.CLIENTE)
        }
    
    # Crear instancias de repositorios con el engine de test
    compra_repo = CompraRepository()
    usuario_repo = UsuarioRepository()
    producto_repo = ProductoRepository()
    envio_repo = EnvioRepository()
    
    # Crear servicios
    compra_service = CompraService(compra_repo, usuario_repo, producto_repo)
    usuario_service = UsuarioService(usuario_repo)
    producto_service = ProductoService(producto_repo)
    envio_service = EnvioService(envio_repo, producto_repo)
    
    # Override de dependencias
    import deps
    app.dependency_overrides[get_current_user] = mock_get_current_user
    app.dependency_overrides[deps.get_compra_service] = lambda: compra_service
    app.dependency_overrides[deps.get_usuario_service] = lambda: usuario_service
    app.dependency_overrides[deps.get_producto_service] = lambda: producto_service
    app.dependency_overrides[deps.get_envio_service] = lambda: envio_service
    
    # Registrar routers
    app.include_router(compra_router)
    app.include_router(envio_router)
    
    # Parchear engine y session
    with patch('infraestructure.db.engine.engine', test_engine):
        with patch('infraestructure.db.engine.async_session', test_session_factory):
            # Mock de RabbitMQ
            with patch('infraestructure.broker.publisher_rabbitmq._get_connection') as mock_conn:
                mock_channel = MagicMock()
                mock_conn.return_value.channel.return_value = mock_channel
                
                yield app
    
    app.dependency_overrides.clear()


@pytest.fixture
async def integration_client(app_with_test_db):
    """Cliente HTTP asíncrono para pruebas."""
    transport = ASGITransport(app=app_with_test_db)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
async def seed_data(test_engine, test_session_factory):
    """Inserta datos de prueba en la base de datos."""
    async with test_session_factory() as session:
        # Crear usuarios de prueba
        usuario1 = UsuarioModel(
            u_id=1,
            u_nombre="Cliente Test",
            u_email="cliente@test.com",
            u_es_activo=True
        )
        session.add(usuario1)
        
        usuario2 = UsuarioModel(
            u_id=2,
            u_nombre="Usuario Inactivo",
            u_email="inactivo@test.com",
            u_es_activo=False
        )
        session.add(usuario2)
        
        # Crear productos de prueba
        producto1 = ProductoModel(
            p_id=1,
            p_nombre="Manzanas",
            p_id_gremio=1,
            p_precio=2.50,
            p_unidad="kg",
            p_stock=100
        )
        session.add(producto1)
        
        producto2 = ProductoModel(
            p_id=2,
            p_nombre="Naranjas",
            p_id_gremio=1,
            p_precio=3.00,
            p_unidad="kg",
            p_stock=50
        )
        session.add(producto2)
        
        producto3 = ProductoModel(
            p_id=3,
            p_nombre="Leche",
            p_id_gremio=2,
            p_precio=1.50,
            p_unidad="litro",
            p_stock=200
        )
        session.add(producto3)
        
        await session.commit()
    
    return {
        "usuario_id": 1,
        "usuario_inactivo_id": 2,
        "productos": [1, 2, 3]
    }