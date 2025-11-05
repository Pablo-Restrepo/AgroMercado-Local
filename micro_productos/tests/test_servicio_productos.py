

from unittest.mock import AsyncMock, Mock
from pydantic import ValidationError
import pytest
from pytest_mock import mocker
from application.producto_service import ProductoService
from api.esquemas import ProductoConsulta, ProductoRegistro, ProductorRegistroConsulta

@pytest.fixture
def producto_invalido():
    """
    Fixture que intenta crear un ProductoRegistro con datos inválidos.
    Se usa dentro de pruebas que esperan ValidationError.
    """
    # Este diccionario viola el tipo de 'p_precio' (string en vez de float)
    datos_invalidos = {
        "p_nombre": "Manzanas Fuji",
        "p_tipo": "Fruta",
        "p_unidad": "kg",
        "prod_id": 101,
        "img": "/9j/4AAQSkZJRgABAQEASABIAAD//2Q==",
        "p_precio": "precio_invalido"  # tipo incorrecto
    }
    return datos_invalidos

@pytest.mark.asyncio
async def test_registrar_producto_invalido(servicio, producto_invalido):
    with pytest.raises(ValidationError):
        # Forzamos la validación creando el modelo explícitamente
        producto = ProductoRegistro(**producto_invalido)
        await servicio.registrar_producto(producto)

@pytest.fixture
def id():
    return 1
@pytest.fixture
def prod_id(): 
    return 1
@pytest.fixture
def id_gremio():
    return 101
@pytest.fixture
def productor():
    productor1 = ProductorRegistroConsulta(
    prod_id=1,
    prod_nombre="Carlos",
    prod_apellido="Ramírez",
    prod_cod_gremio=101,
    prod_nombre_gremio="Asociación de Fruticultores del Valle"  
    )
    return productor1
@pytest.fixture
def productores():
    productor1 = ProductorRegistroConsulta(
    prod_id=1,
    prod_nombre="Carlos",
    prod_apellido="Ramírez",
    prod_cod_gremio=101,
    prod_nombre_gremio="Asociación de Fruticultores del Valle"  
    )

    productor2 = ProductorRegistroConsulta(
        prod_id=2,
        prod_nombre="María",
        prod_apellido="González",
        prod_cod_gremio=102,
        prod_nombre_gremio="Cooperativa de Lácteos del Sur"
    )

    productor3 = ProductorRegistroConsulta(
        prod_id=3,
        prod_nombre="José",
        prod_apellido="López",
        prod_cod_gremio=103,
        prod_nombre_gremio="Gremio de Productores de Granos Andinos"
    )

    productor4 = ProductorRegistroConsulta(
        prod_id=4,
        prod_nombre="Ana",
        prod_apellido="Torres",
        prod_cod_gremio=104,
        prod_nombre_gremio="Asociación de Avicultores Regionales"
    )

    productor5 = ProductorRegistroConsulta(
        prod_id=5,
        prod_nombre="Luis",
        prod_apellido="Martínez",
        prod_cod_gremio=105,
        prod_nombre_gremio="Cooperativa Cafetera Nacional"
    )

    productores = [productor1, productor2, productor3, productor4, productor5]
    return productores
@pytest.fixture
def productos_consulta():
    producto1 = ProductoConsulta(
    p_nombre="Manzanas Fuji",
    p_tipo="Fruta",
    p_unidad="kg",
    gre_nombre="Asociación de Fruticultores del Valle",
    p_precio=3.5,
    img="/9j/4AAQSkZJRgABAQEASABIAAD//2Q==" 
    )

    producto2 = ProductoConsulta(
        p_nombre="Leche Deslactosada",
        p_tipo="Lácteo",
        p_unidad="litro",
        gre_nombre="Cooperativa de Lácteos del Sur",
        p_precio=1.8,
        img="iVBORw0KGgoAAAANSUhEUgAAAAUA//8AAABCAQEA"
    )

    producto3 = ProductoConsulta(
        p_nombre="Arroz Premium",
        p_tipo="Grano",
        p_unidad="kg",
        gre_nombre="Gremio de Productores de Granos Andinos",
        p_precio=2.2,
        img="AAAFBfj42Pj4+AAAABJRU5ErkJggg=="
    )

    producto4 = ProductoConsulta(
        p_nombre="Huevos Orgánicos",
        p_tipo="Proteína",
        p_unidad="docena",
        gre_nombre="Asociación de Avicultores Regionales",
        p_precio=4.0,
        img="/9j/2wCEAAgGBgcGBQgHBwcJCQgKDBQNDAsL"
    )

    producto5 = ProductoConsulta(
        p_nombre="Café Molido 500g",
        p_tipo="Bebida",
        p_unidad="paquete",
        gre_nombre="Cooperativa Cafetera Nacional",
        p_precio=7.5,
        img="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ"
    )

    productos_consulta = [producto1, producto2, producto3, producto4, producto5]
    return productos_consulta
@pytest.fixture
def productos():
    producto1 = ProductoRegistro(
    p_nombre="Manzanas Fuji",
    p_tipo="Fruta",
    p_unidad="kg",
    prod_id=101,
    img="/9j/4AAQSkZJRgABAQEASABIAAD//2Q==",
    p_precio=3.5
    )

    producto2 = ProductoRegistro(
        p_nombre="Leche Deslactosada",
        p_tipo="Lácteo",
        p_unidad="litro",
        prod_id=102,
        img="iVBORw0KGgoAAAANSUhEUgAAAAUA//8AAABCAQEA",
        p_precio=1.8
    )

    producto3 = ProductoRegistro(
        p_nombre="Arroz Premium",
        p_tipo="Grano",
        p_unidad="kg",
        prod_id=103,
        img="AAAFBfj42Pj4+AAAABJRU5ErkJggg==",
        p_precio=2.2
    )

    producto4 = ProductoRegistro(
        p_nombre="Huevos Orgánicos",
        p_tipo="Proteína",
        p_unidad="docena",
        prod_id=104,
        img="/9j/2wCEAAgGBgcGBQgHBwcJCQgKDBQNDAsL",
        p_precio=4.0
    )

    producto5 = ProductoRegistro(
        p_nombre="Café Molido 500g",
        p_tipo="Bebida",
        p_unidad="paquete",
        prod_id=105,
        img="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ",
        p_precio=7.5
    )


    productos = [producto1, producto2, producto3, producto4, producto5]
    return productos

@pytest.fixture
def producto_actualizado():
    producto = ProductoRegistro(
                p_nombre="Manzanas verdes",
                p_tipo="Fruta",
                p_unidad="kg",
                prod_id=101,
                img="/9j/4AAQSkZJRgABAQEASABIAAD//2Q==",
                p_precio=3.5
                )
    return producto
@pytest.fixture
def producto_valido():
    producto1 = ProductoRegistro(
                p_nombre="Manzanas Fuji",
                p_tipo="Fruta",
                p_unidad="kg",
                prod_id=101,
                img="/9j/4AAQSkZJRgABAQEASABIAAD//2Q==",
                p_precio=3.5
                )
    return producto1
@pytest.fixture
def servicio(productos_consulta,id):
    repo_comandos = AsyncMock()
    repo_comandos.save_producto.return_value = id
    repo_comandos.save_productor.return_value = id
    repo_comandos.edit_producto.return_value = id
    repo_comandos.delete_producto.return_value = id
    repo_consultas = Mock()
    repo_consultas.list_productos_por_gremio.return_value = productos_consulta[0]
    repo_consultas.list_productos_por_productor.return_value = productos_consulta[0]
    repo_consultas.get_producto_por_id.return_value = productos_consulta[0]
    repo_consultas.list_all_productos.return_value = productos_consulta
    servicio = ProductoService(command_repo=repo_comandos, query_repo=repo_consultas)
    return servicio

@pytest.mark.asyncio
async def test_registrar_producto(servicio,producto_valido):
    resultado = await servicio.registrar_producto(producto_valido)

    assert resultado == 1

@pytest.mark.asyncio
async def test_registrar_productor(servicio,productor):
    resultado = await servicio.registrar_productor(productor)
    
    assert resultado == 1

@pytest.mark.asyncio
async def test_eliminar_producto(servicio):
    resultado = await servicio.eliminar_producto(1)
    assert resultado == 1
@pytest.mark.asyncio
async def test_editar_producto(servicio,id,producto_actualizado):
    resultado = await servicio.editar_producto(id,producto_actualizado)

    assert resultado == 1


def test_listar_todos_los_productos(servicio, productos_consulta):
    resultado = servicio.listar_todos_los_productos()

    assert isinstance(resultado, list)
    assert len(resultado) == len(productos_consulta)
    assert resultado[0].p_nombre == productos_consulta[0].p_nombre


def test_listar_productos_por_gremio(servicio, id_gremio, productos_consulta):
    resultado = servicio.listar_productos_por_gremio(id_gremio)

    assert resultado == productos_consulta[0]


def test_obtener_producto_por_id(servicio, id, productos_consulta):
    resultado = servicio.obtener_producto_por_id(id)

    assert resultado == productos_consulta[0]


def test_listar_productos_por_productor(servicio, prod_id, productos_consulta):
    resultado = servicio.listar_productos_por_productor(prod_id)

    assert resultado == productos_consulta[0]


@pytest.mark.asyncio
async def test_editar_producto_inexistente(servicio, producto_actualizado):
    # Simula que el comando no encuentra el producto
    servicio.command_repo.edit_producto.return_value = 0

    resultado = await servicio.editar_producto(999, producto_actualizado)

    assert resultado == 0

@pytest.mark.asyncio
async def test_eliminar_producto_inexistente(servicio):
    # Simula que el producto no existe
    servicio.command_repo.delete_producto.return_value = 0

    resultado = await servicio.eliminar_producto(999)
    assert resultado == 0
