import pytest
import pytest_asyncio
from unittest.mock import patch, MagicMock
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

from infraestructure.db.modelsSQL import (
    UsuarioModel, ProductoModel, CompraModel, 
    ProductoUnitarioModel, EnvioModel
)

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture
def auth_headers_cliente():
    return {"X-Test-Role": "cliente", "X-Test-User-Id": "1"}

@pytest.fixture
def auth_headers_productor():
    return {"X-Test-Role": "productor-admin", "X-Test-User-Id": "2"}

@pytest.fixture
def seed_data():
    return {"usuario_id": 1, "productos": [1, 2, 3]}

# Usamos pytest_asyncio.fixture para ser explícitos y evitar problemas de detección
@pytest_asyncio.fixture(scope="function")
async def integration_client():
    """
    Crea un entorno de prueba aislado:
    - Nueva DB en memoria
    - Nuevos datos semilla
    - Nueva instancia de FastAPI
    - Mocks de RabbitMQ y Auth
    """
    # --- A. Configurar DB ---
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool, 
    )
    
    # Crear tablas
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    # --- B. Insertar Datos Semilla ---
    async with session_factory() as session:
        # Usuarios
        session.add(UsuarioModel(u_id=1, u_nombre="Cliente", u_email="c@test.com", u_es_activo=True))
        session.add(UsuarioModel(u_id=2, u_nombre="Inactivo", u_email="i@test.com", u_es_activo=False))
        
        # Productos (Stock fresco para cada test)
        session.add(ProductoModel(p_id=1, p_nombre="P1", p_id_gremio=1, p_precio=10.0, p_unidad="u", p_stock=100))
        session.add(ProductoModel(p_id=2, p_nombre="P2", p_id_gremio=1, p_precio=20.0, p_unidad="u", p_stock=50))
        session.add(ProductoModel(p_id=3, p_nombre="P3", p_id_gremio=2, p_precio=30.0, p_unidad="u", p_stock=50))
        
        await session.commit()

    # --- C. Configurar App y Mocks ---
    from fastapi import FastAPI, Request
    from api.compra_controller import router as compra_router
    from api.envio_controller import router as envio_router
    from api.exceptions import register_exception_handlers
    from core.auth_middleware import get_current_user
    from domain.entities.usuario import RolEnum
    import deps
    from infraestructure.repositories import CompraRepository, UsuarioRepository, ProductoRepository, EnvioRepository
    from application.services import CompraService, UsuarioService, ProductoService, EnvioService

    app = FastAPI()
    register_exception_handlers(app)

    # Mock Auth
    def mock_get_current_user(request: Request):
        role_str = request.headers.get("X-Test-Role", "cliente")
        uid = int(request.headers.get("X-Test-User-Id", "1"))
        role_enum = {
            "cliente": RolEnum.CLIENTE,
            "productor-admin": RolEnum.PRODUCTOR_ADMIN
        }.get(role_str, RolEnum.CLIENTE)
        
        return {"id": uid, "user_id": uid, "sub": uid, "email": "test@test.com", "rol": role_enum}

    # Resetear Singletons
    deps._singleton_compra_repo = None
    deps._singleton_usuario_repo = None
    deps._singleton_producto_repo = None
    deps._singleton_envio_repo = None
    
    # Crear servicios frescos
    compra_repo = CompraRepository()
    usuario_repo = UsuarioRepository()
    producto_repo = ProductoRepository()
    envio_repo = EnvioRepository()
    
    compra_svc = CompraService(compra_repo, usuario_repo, producto_repo)
    usuario_svc = UsuarioService(usuario_repo)
    producto_svc = ProductoService(producto_repo)
    envio_svc = EnvioService(envio_repo, producto_repo)

    app.dependency_overrides[get_current_user] = mock_get_current_user
    app.dependency_overrides[deps.get_compra_service] = lambda: compra_svc
    app.dependency_overrides[deps.get_usuario_service] = lambda: usuario_svc
    app.dependency_overrides[deps.get_producto_service] = lambda: producto_svc
    app.dependency_overrides[deps.get_envio_service] = lambda: envio_svc

    app.include_router(compra_router)
    app.include_router(envio_router)

    # --- D. Parchear y Ejecutar ---
    with patch('infraestructure.db.engine.engine', engine), \
         patch('infraestructure.repositories.async_session', session_factory), \
         patch('infraestructure.broker.publisher_rabbitmq._get_connection') as mock_conn, \
         patch('infraestructure.broker.publisher_rabbitmq.pika') as mock_pika:
        
        mock_channel = MagicMock()
        mock_conn.return_value.channel.return_value = mock_channel
        mock_pika.BlockingConnection.return_value = MagicMock()

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client

    # --- E. Limpieza ---
    app.dependency_overrides.clear()
    await engine.dispose()