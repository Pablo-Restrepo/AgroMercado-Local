import pytest
from domain.models import Productor, Gremio, RolEnum


def test_productor_initialization_and_attributes():
    p = Productor(id=1, codigo="P001", nombres="Ana", apellidos="Lopez")
    assert p.id == 1
    assert p.codigo == "P001"
    assert p.nombres == "Ana"
    assert p.apellidos == "Lopez"
    assert p.id_gremio is None
    assert p.rol is None
    assert p.es_activo is True
    assert p.u_id is None


def test_eliminar_productor_sets_inactive_and_clears_gremio():
    p = Productor(id=2, codigo="P002", nombres="Luis", apellidos="Perez", id_gremio=5, es_activo=True)
    p.eliminar_productor()
    assert p.es_activo is False
    assert p.id_gremio is None


def test_crear_gremio_raises_if_not_admin():
    p = Productor(id=3, codigo="P003", nombres="NoAdmin", apellidos="User", rol=RolEnum.PRODUCTOR_AFILIADO)
    with pytest.raises(ValueError, match="Solo un productor con rol ADMIN"):
        p.crear_gremio("GremioX")


def test_crear_gremio_raises_if_already_in_gremio():
    p = Productor(id=4, codigo="P004", nombres="Admin", apellidos="Exists", rol=RolEnum.PRODUCTOR_ADMIN, id_gremio=10)
    with pytest.raises(ValueError, match="El productor ya pertenece a un gremio"):
        p.crear_gremio("GremioX")


def test_crear_gremio_success_returns_gremio_with_productor_in_list():
    p = Productor(id=5, codigo="P005", nombres="Admin", apellidos="Good", rol=RolEnum.PRODUCTOR_ADMIN)
    g = p.crear_gremio("NuevoGremio")
    assert isinstance(g, Gremio)
    assert g.nombre == "NuevoGremio"
    # creator puts the productor into the gremio.productores list
    assert any(prod.id == p.id for prod in g.productores)
    # note: crear_gremio in domain does not set productor.id_gremio automatically in this code
    assert p.id_gremio is None or p.id_gremio == g.id


def test_gremio_init_requires_nombre():
    with pytest.raises(ValueError, match="Todos los campos son obligatorios"):
        Gremio(id=None, nombre="", productores=None)


def test_gremio_agregar_productor_sets_relations_and_prevents_duplicates():
    g = Gremio(id=20, nombre="GremioTest")
    p = Productor(id=6, codigo="P006", nombres="Mar", apellidos="One")
    g.agregar_productor(p)
    assert g.es_activo is True
    assert any(prod.id == 6 for prod in g.productores)
    # agregar should set productor.id_gremio to gremio.id and rol to afiliado
    assert p.id_gremio == 20
    assert p.rol == RolEnum.PRODUCTOR_AFILIADO
    # duplicate add raises
    with pytest.raises(ValueError, match="El productor ya pertenece al gremio"):
        g.agregar_productor(p)


def test_gremio_remover_productor_removes_and_clears_relations():
    g = Gremio(id=30, nombre="GremioRem")
    p = Productor(id=7, codigo="P007", nombres="Rem", apellidos="One")
    g.agregar_productor(p)
    # ensure it's present
    assert g.es_miembro(p)
    g.remover_productor(p)
    assert not g.es_miembro(p)
    assert p.id_gremio is None
    assert p.rol is None


def test_gremio_remover_admin_raises():
    g = Gremio(id=40, nombre="GremioAdmin")
    admin = Productor(id=8, codigo="P008", nombres="Admin", apellidos="Boss", rol=RolEnum.PRODUCTOR_ADMIN)
    # manual append to simulate existing admin in list
    g.productores.append(admin)
    with pytest.raises(ValueError, match="No se puede remover al administrador del gremio"):
        g.remover_productor(admin)


def test_gremio_es_miembro_and_obtener_admin_behavior():
    g = Gremio(id=50, nombre="GremioMembers")
    p1 = Productor(id=9, codigo="P009", nombres="A", apellidos="A")
    p2 = Productor(id=10, codigo="P010", nombres="B", apellidos="B", rol=RolEnum.PRODUCTOR_ADMIN)
    g.agregar_productor(p1)
    # manually add admin so agregar_productor doesn't override role
    g.productores.append(p2)
    assert g.es_miembro(p1) is True
    assert g.es_miembro(p2) is True
    admin_found = g.obtener_admin()
    assert admin_found is p2
    # if no admin present, obtener_admin returns None
    g2 = Gremio(id=51, nombre="NoAdmin")
    assert g2.obtener_admin() is None