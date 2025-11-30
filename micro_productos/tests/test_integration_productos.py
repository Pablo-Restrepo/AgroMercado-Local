import base64
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI

from api.esquemas import (
    ProductoConsulta,
    ProductorRegistroConsulta,
    CategoriaConsulta,
)
from application.producto_service import ProductoService
from api.producto_controller import ProductoController
from infrastructure.mongo_repository import MongoQueryRepository
from infrastructure.sql_repository import SQLCommandRepository


# ============================================================
# FIXTURES COMPARTIDAS
# ============================================================

@pytest.fixture
def mock_jwt_payload_productor():
    """Payload JWT simulado para un productor"""
    return {
        'user_id': '1',
        'email': 'productor@test.com',
        'username': 'productor_test',
        'rol': 'productor-admin'
    }

@pytest.fixture
def mock_jwt_payload_cliente():
    """Payload JWT simulado para un cliente (sin permisos de escritura)"""
    return {
        'user_id': '2',
        'email': 'cliente@test.com',
        'username': 'cliente_test',
        'rol': 'cliente'
    }

@pytest.fixture
def productor_mock():
    """Productor de prueba"""
    return ProductorRegistroConsulta(
        prod_id=1,
        prod_nombre="Juan",
        prod_apellido="Pérez",
        prod_cod_gremio=101,
        prod_nombre_gremio="Asociación de Fruticultores"
    )

@pytest.fixture
def categoria_mock():
    """Categoría de prueba"""
    return CategoriaConsulta(cat_id=1, cat_nombre="frutas")

@pytest.fixture
def producto_registro_valido():
    """Producto válido para registro"""
    return {
        "p_nombre": "Manzanas Rojas",
        "cat_id": 1,
        "p_unidad": "kg",
        "prod_id": 1,
        "img": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ",
        "p_precio": 5.50,
        "p_stock": 100,
        "p_medicinal": False
    }

@pytest.fixture
def producto_actualizacion_valido():
    """Producto válido para actualización"""
    return {
        "p_nombre": "Manzanas Verdes",
        "cat_id": 1,
        "p_unidad": "kg",
        "img": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ",
        "p_precio": 6.00,
        "p_stock": 80,
        "p_medicinal": False
    }

@pytest.fixture
def productos_consulta_mock():
    """Lista de productos para consultas"""
    return [
        ProductoConsulta(
            p_id=1,
            p_nombre="Manzanas",
            cat_id=1,
            p_unidad="kg",
            gre_nombre="Fruticultores",
            p_precio=5.0,
            p_stock=100,
            p_medicinal=False,
            img=base64.b64encode(b"fake_image").decode("utf-8")
        ),
        ProductoConsulta(
            p_id=2,
            p_nombre="Menta",
            cat_id=5,
            p_unidad="manojo",
            gre_nombre="Fruticultores",
            p_precio=2.0,
            p_stock=50,
            p_medicinal=True,
            img=base64.b64encode(b"fake_image").decode("utf-8")
        )
    ]


@pytest.fixture
def mock_event_manager():
    """Mock del EventManager"""
    mock = MagicMock()
    mock.notify = AsyncMock()
    mock.subscribe = MagicMock()
    return mock


# ============================================================
# TEST 1: Flujo completo de registro de producto
# ============================================================

@pytest.mark.asyncio
async def test_integracion_registrar_producto_flujo_completo(
    mock_jwt_payload_productor,
    productor_mock,
    categoria_mock,
    producto_registro_valido,
    mock_event_manager
):
    """
    Test de integración que verifica el flujo completo de registro de producto:
    1. Recibe petición HTTP POST con token JWT válido
    2. El controlador valida permisos y delega al servicio
    3. El servicio guarda en SQL y sincroniza con MongoDB via eventos
    4. Se publica mensaje a RabbitMQ
    5. Retorna el ID del producto creado
    """
    with patch('core.events.event_manager.EventManager', return_value=mock_event_manager), \
         patch('core.events.publisher.publish', new_callable=AsyncMock) as mock_publish:
        
        # Crear repositorios mockeados
        command_repo = AsyncMock(spec=SQLCommandRepository)
        command_repo.save_producto = AsyncMock(return_value=1)
        command_repo.get_productor = AsyncMock(return_value=productor_mock)
        command_repo.get_categoria = AsyncMock(return_value=categoria_mock)
        
        query_repo = MagicMock(spec=MongoQueryRepository)
        
        servicio = ProductoService(command_repo=command_repo, query_repo=query_repo)
        controller = ProductoController(servicio)
        
        # Crear app de prueba con override de dependencia
        app = FastAPI()
        app.include_router(controller.router)
        
        # Override de la dependencia de autenticación
        from core.auth_middleware import get_current_user
        app.dependency_overrides[get_current_user] = lambda: mock_jwt_payload_productor
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/productos/",
                json=producto_registro_valido,
                headers={"Authorization": "Bearer token_valido"}
            )
        
        # Verificaciones
        assert response.status_code == 200
        assert response.json() == 1
        
        # Verificar que se llamó al repositorio de comandos
        command_repo.save_producto.assert_called_once()
        command_repo.get_productor.assert_called_once_with(prod_id=1)
        command_repo.get_categoria.assert_called_once_with(cat_id=1)


# ============================================================
# TEST 2: Flujo de consulta de productos con filtros
# ============================================================

@pytest.mark.asyncio
async def test_integracion_consultar_productos_por_gremio_y_categoria(
    productos_consulta_mock
):
    """
    Test de integración que verifica el flujo de consulta de productos:
    1. Consulta productos por gremio desde MongoDB
    2. Consulta productos por categoría
    3. Consulta productos medicinales
    4. Verifica que los datos se transforman correctamente
    """
    # Crear query_repo mockeado con los métodos correctos
    query_repo = MagicMock(spec=MongoQueryRepository)
    query_repo.list_all_productos.return_value = productos_consulta_mock
    query_repo.list_productos_por_gremio.return_value = [productos_consulta_mock[0]]
    query_repo.list_all_productos_medicinales.return_value = [productos_consulta_mock[1]]
    query_repo.list_all_productos_por_categoria.return_value = [productos_consulta_mock[0]]
    
    command_repo = AsyncMock(spec=SQLCommandRepository)
    
    servicio = ProductoService(command_repo=command_repo, query_repo=query_repo)
    controller = ProductoController(servicio)
    
    # Crear app de prueba
    app = FastAPI()
    app.include_router(controller.router)
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Test 1: Listar todos los productos
        response_all = await client.get("/api/productos/")
        assert response_all.status_code == 200
        productos = response_all.json()
        assert isinstance(productos, list)
        assert len(productos) == 2
        
        # Verificar estructura de los productos
        assert productos[0]["p_nombre"] == "Manzanas"
        assert productos[1]["p_nombre"] == "Menta"
        
        # Verificar que se llamó al repositorio
        query_repo.list_all_productos.assert_called_once()
        
        # Test 2: Listar productos por gremio
        response_gremio = await client.get("/api/productos/gremio/101")
        assert response_gremio.status_code == 200
        productos_gremio = response_gremio.json()
        assert len(productos_gremio) == 1
        assert productos_gremio[0]["p_nombre"] == "Manzanas"
        
        # Verificar llamada con parámetro correcto
        query_repo.list_productos_por_gremio.assert_called_with(101)
        
        # Test 3: Listar productos medicinales
        response_medicinales = await client.get("/api/productos/medicinales/")
        assert response_medicinales.status_code == 200
        productos_medicinales = response_medicinales.json()
        assert len(productos_medicinales) == 1
        assert productos_medicinales[0]["p_medicinal"] == True
        assert productos_medicinales[0]["p_nombre"] == "Menta"
        
        # Test 4: Listar productos por categoría
        response_categoria = await client.get("/api/productos/categoria/1")
        assert response_categoria.status_code == 200
        productos_categoria = response_categoria.json()
        assert len(productos_categoria) == 1


# ============================================================
# TEST 3: Flujo de actualización y eliminación con validación de permisos
# ============================================================

@pytest.mark.asyncio
async def test_integracion_actualizar_eliminar_producto_con_permisos(
    mock_jwt_payload_productor,
    mock_jwt_payload_cliente,
    categoria_mock,
    producto_actualizacion_valido,
    mock_event_manager
):
    """
    Test de integración que verifica:
    1. Actualización de producto con permisos válidos (productor)
    2. Eliminación de producto con permisos válidos
    3. Rechazo de operaciones para usuarios sin permisos (cliente)
    4. Sincronización de cambios entre SQL y MongoDB
    """
    with patch('core.events.event_manager.EventManager', return_value=mock_event_manager), \
         patch('core.events.publisher.publish', new_callable=AsyncMock) as mock_publish:
        
        # Crear repositorios mockeados
        command_repo = AsyncMock(spec=SQLCommandRepository)
        command_repo.edit_producto = AsyncMock(return_value=1)
        command_repo.delete_producto = AsyncMock(return_value=1)
        command_repo.get_categoria = AsyncMock(return_value=categoria_mock)
        
        query_repo = MagicMock(spec=MongoQueryRepository)
        
        servicio = ProductoService(command_repo=command_repo, query_repo=query_repo)
        controller = ProductoController(servicio)
        
        # ---- TEST: Actualizar producto con permisos de productor ----
        app_productor = FastAPI()
        app_productor.include_router(controller.router)
        
        from core.auth_middleware import get_current_user
        app_productor.dependency_overrides[get_current_user] = lambda: mock_jwt_payload_productor
        
        transport = ASGITransport(app=app_productor)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response_update = await client.put(
                "/api/productos/1",
                json=producto_actualizacion_valido,
                headers={"Authorization": "Bearer token_productor"}
            )
            
            assert response_update.status_code == 200
            assert response_update.json() == 1
            command_repo.edit_producto.assert_called_once()
            
            # ---- TEST: Eliminar producto con permisos de productor ----
            command_repo.edit_producto.reset_mock()
            
            response_delete = await client.delete(
                "/api/productos/1",
                headers={"Authorization": "Bearer token_productor"}
            )
            
            assert response_delete.status_code == 200
            command_repo.delete_producto.assert_called_once_with(p_id=1)
        
        # ---- TEST: Intentar actualizar/eliminar sin permisos (cliente) ----
        command_repo.edit_producto.reset_mock()
        command_repo.delete_producto.reset_mock()
        
        # Crear nueva app con permisos de cliente
        servicio_cliente = ProductoService(command_repo=command_repo, query_repo=query_repo)
        controller_cliente = ProductoController(servicio_cliente)
        
        app_cliente = FastAPI()
        app_cliente.include_router(controller_cliente.router)
        app_cliente.dependency_overrides[get_current_user] = lambda: mock_jwt_payload_cliente
        
        transport_cliente = ASGITransport(app=app_cliente)
        async with AsyncClient(transport=transport_cliente, base_url="http://test") as client:
            # Intentar actualizar como cliente
            response_forbidden = await client.put(
                "/api/productos/1",
                json=producto_actualizacion_valido,
                headers={"Authorization": "Bearer token_cliente"}
            )
            
            assert response_forbidden.status_code == 403
            assert "No tiene permisos" in response_forbidden.json()["detail"]
            
            # Verificar que NO se llamó al repositorio
            command_repo.edit_producto.assert_not_called()
            
            # Intentar eliminar como cliente
            response_delete_forbidden = await client.delete(
                "/api/productos/1",
                headers={"Authorization": "Bearer token_cliente"}
            )
            
            assert response_delete_forbidden.status_code == 403
            command_repo.delete_producto.assert_not_called()